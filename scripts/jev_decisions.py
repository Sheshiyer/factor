#!/usr/bin/env python3
"""Jev shadow validation and lossless context compaction.

Functions:
    validate_decision(candidates, result, min_confidence=0.5) -> dict
        Validate a Jev decision result against the supplied candidate IDs.
        Returns an explicit status dict; never raises on validation failure.

    compact_context(messages, keep_ids, ranking_ok) -> list[dict]
        Compact a message list, preserving kept IDs and protected entries.
        Falls back to the original list when ranking is unavailable.
"""

from __future__ import annotations

import math
import sys
from typing import Any

# ---------------------------------------------------------------------------
# validate_decision
# ---------------------------------------------------------------------------

# Statuses returned in the status dict
STATUS_ACCEPTED = "accepted"
STATUS_ABSTAINED = "abstained"
STATUS_LOW_CONFIDENCE = "low_confidence"
STATUS_INVALID_CANDIDATE = "invalid_candidate"
STATUS_INVALID_CONFIDENCE = "invalid_confidence"
STATUS_MISSING_RECEIPT = "missing_receipt"
STATUS_SYNTHETIC = "synthetic"
STATUS_DISABLED = "disabled"
STATUS_UNAVAILABLE = "unavailable"
STATUS_TIMEOUT = "timeout"

# Outcome types that indicate a genuine decision was not reached
_NON_DECISION_OUTCOMES = frozenset(
    {"disabled", "unavailable", "timeout", "abstain", "abstained"}
)

# Fields a real (non-synthetic) result must supply for provenance
_RECEIPT_FIELDS = ("provider", "model")

# Protected message categories that must not be dropped during compaction
_PROTECTED_ROLES = frozenset({"system", "developer"})
_PROTECTED_CONTENT_MARKERS = (
    "do not",
    "must not",
    "prohibited",
    "commitment",
    "unresolved question",
    "path:",
    "never ",
    "?",
    "/",
    "\\",
)


def validate_decision(
    candidates: list[str],
    result: dict[str, Any],
    min_confidence: float = 0.5,
) -> dict[str, Any]:
    """Validate a Jev shadow-decision result.

    Parameters
    ----------
    candidates:
        List of candidate IDs that were offered to Jev.
    result:
        The decision result dict.  Expected keys:
        - ``outcome``:    str — the chosen candidate id, "abstain", or a
                           non-decision keyword (disabled/unavailable/timeout)
        - ``confidence``: float in [0, 1] — required for real decisions
        - ``provider``:   str — required for real (non-synthetic) results
        - ``model``:      str — required for real (non-synthetic) results
        - ``synthetic``:  bool (optional) — marks a local fixture
        - ``shadow_only``: bool (optional) — marks shadow-mode results

    Returns
    -------
    dict with keys:
    - ``status``: one of the STATUS_* constants
    - ``outcome``: the original outcome value (or None)
    - ``confidence``: the original confidence value (or None)
    - ``synthetic``: bool
    - ``shadow_only``: bool
    - ``reason``: human-readable explanation
    """
    if not isinstance(result, dict):
        return {"status": "invalid_result", "reason": "result must be an object", "shadow_only": True}
    if "outcome" not in result:
        return {"status": "invalid_result", "reason": "outcome is required", "shadow_only": True}
    if not isinstance(candidates, list) or any(not isinstance(c, str) or not c.strip() or c in _NON_DECISION_OUTCOMES for c in candidates) or len(set(candidates)) != len(candidates):
        return {"status": STATUS_INVALID_CANDIDATE, "reason": "invalid candidate list", "shadow_only": True}
    if isinstance(min_confidence, bool) or not isinstance(min_confidence, (int, float)) or not 0 <= min_confidence <= 1 or not math.isfinite(min_confidence):
        return {"status": STATUS_INVALID_CONFIDENCE, "reason": "invalid confidence threshold", "shadow_only": True}
    if any(key in result and not isinstance(result[key], bool) for key in ("synthetic", "shadow_only")):
        return {"status": "invalid_result", "reason": "flags must be booleans", "shadow_only": True}
    outcome = result.get("outcome")
    confidence = result.get("confidence")
    is_synthetic = bool(result.get("synthetic", False))
    is_shadow = True

    base = {
        "outcome": outcome,
        "confidence": confidence,
        "synthetic": is_synthetic,
        "shadow_only": is_shadow,
    }

    # --- non-decision outcomes ---
    if outcome is not None and not isinstance(outcome, str):
        return {**base, "status": STATUS_INVALID_CANDIDATE, "reason": "outcome must be a candidate string"}
    if outcome in _NON_DECISION_OUTCOMES or outcome is None:
        status = STATUS_ABSTAINED if outcome in {"abstain", "abstained"} else (
            STATUS_DISABLED if outcome == "disabled" else
            STATUS_UNAVAILABLE if outcome == "unavailable" else
            STATUS_TIMEOUT if outcome == "timeout" else
            STATUS_ABSTAINED  # None treated as abstain
        )
        return {**base, "status": status, "reason": f"non-decision outcome: {outcome!r}"}

    # --- validate confidence ---
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return {
            **base,
            "status": STATUS_INVALID_CONFIDENCE,
            "reason": "confidence is missing or not a number",
        }
    if isinstance(confidence, float) and not math.isfinite(confidence):
        return {
            **base,
            "status": STATUS_INVALID_CONFIDENCE,
            "reason": f"confidence must be finite, got {confidence!r}",
        }
    if not (0.0 <= confidence <= 1.0):
        return {
            **base,
            "status": STATUS_INVALID_CONFIDENCE,
            "reason": f"confidence {confidence!r} is out of [0, 1]",
        }

    # --- validate candidate ---
    if outcome not in candidates:
        return {
            **base,
            "status": STATUS_INVALID_CANDIDATE,
            "reason": f"outcome {outcome!r} is not in candidates {candidates!r}",
        }

    # --- provenance receipt for real results ---
    if not is_synthetic:
        missing = [f for f in _RECEIPT_FIELDS if not isinstance(result.get(f), str) or not result[f].strip()]
        if missing:
            return {
                **base,
                "status": STATUS_MISSING_RECEIPT,
                "reason": f"non-synthetic result missing receipt fields: {missing!r}",
            }

    # --- synthetic label ---
    if is_synthetic:
        if confidence < min_confidence:
            return {
                **base,
                "status": STATUS_LOW_CONFIDENCE,
                "reason": (
                    f"synthetic result confidence {confidence!r} "
                    f"below minimum {min_confidence!r}"
                ),
            }
        return {
            **base,
            "status": STATUS_SYNTHETIC,
            "reason": "synthetic local fixture; no provider call implied",
        }

    # --- low confidence ---
    if confidence < min_confidence:
        return {
            **base,
            "status": STATUS_LOW_CONFIDENCE,
            "reason": (
                f"confidence {confidence!r} below minimum {min_confidence!r}"
            ),
        }

    # --- accepted ---
    return {
        **base,
        "status": STATUS_ACCEPTED,
        "reason": "decision accepted",
        "provider": result.get("provider"),
        "model": result.get("model"),
    }


# ---------------------------------------------------------------------------
# compact_context
# ---------------------------------------------------------------------------

def _is_protected(message: dict[str, Any]) -> bool:
    """Return True if a message must not be dropped."""
    if any(message.get(key) for key in ("protected", "prohibition", "commitment", "path", "unresolved_question")):
        return True
    if not isinstance(message.get("content", ""), str):
        return True
    if not isinstance(message.get("role", ""), str):
        return True
    if message.get("role") in _PROTECTED_ROLES:
        return True
    content = str(message.get("content", "")).lower()
    for marker in _PROTECTED_CONTENT_MARKERS:
        if marker in content:
            return True
    return False


def compact_context(
    messages: list[dict[str, Any]],
    keep_ids: list[str],
    ranking_ok: bool,
) -> list[dict[str, Any]]:
    """Compact *messages*, keeping entries in *keep_ids* and protected entries.

    Parameters
    ----------
    messages:
        List of message dicts.  Each may have an ``id`` key.
    keep_ids:
        IDs of messages that must be retained regardless.
    ranking_ok:
        If True, the caller asserts that ranking is available and compaction
        may drop non-kept, non-protected messages.
        If False, ranking is unavailable; return the original list unchanged
        (lossless full fallback).

    Rules
    -----
    - If ``ranking_ok`` is False → return original list unchanged.
    - Protected messages (system role, prohibition/commitment/path/unresolved
      question content) are always kept.
    - Messages with an id in ``keep_ids`` are always kept.
    - The original message dict bytes are preserved (no mutation).
    - Order of surviving messages follows their original order.
    """
    if ranking_ok is not True:
        return list(messages)
    if not isinstance(keep_ids, list) or any(not isinstance(x, str) or not x for x in keep_ids):
        return list(messages)
    if any(not isinstance(m, dict) or not isinstance(m.get("id"), str) or not m["id"] for m in messages):
        return list(messages)
    ids = [m["id"] for m in messages]
    if len(ids) != len(set(ids)) or not set(keep_ids).issubset(ids):
        # Full fallback: preserve all original messages
        return list(messages)

    keep_set = set(keep_ids)
    result: list[dict[str, Any]] = []
    for msg in messages:
        msg_id = msg.get("id")
        if msg_id in keep_set or _is_protected(msg):
            result.append(msg)

    # If compaction would drop everything, return original (safety net)
    if not result and messages:
        return list(messages)

    return result


# ---------------------------------------------------------------------------
# CLI (lightweight, for smoke testing)
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    import json as _json

    if len(argv) < 2:
        print(
            "usage: jev_decisions.py validate-decision <json-result> <candidate,...>\n"
            "       jev_decisions.py compact-context <json-messages> <keep-id,...> ranking_ok|ranking_fail",
            file=sys.stderr,
        )
        return 2

    subcmd = argv[1]

    if subcmd == "validate-decision":
        if len(argv) < 4:
            print("usage: jev_decisions.py validate-decision <json-result> <candidate,...>",
                  file=sys.stderr)
            return 2
        try:
            result_obj = _json.loads(argv[2])
            candidates_list = [c.strip() for c in argv[3].split(",") if c.strip()]
        except (_json.JSONDecodeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        status_dict = validate_decision(candidates_list, result_obj)
        print(_json.dumps(status_dict, indent=2))
        return 0

    if subcmd == "compact-context":
        if len(argv) < 5:
            print("usage: jev_decisions.py compact-context <json-messages> <keep-id,...> ranking_ok|ranking_fail",
                  file=sys.stderr)
            return 2
        try:
            msgs = _json.loads(argv[2])
            keep = [k.strip() for k in argv[3].split(",") if k.strip()]
        except (_json.JSONDecodeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        ranking = argv[4].lower() == "ranking_ok"
        compacted = compact_context(msgs, keep, ranking)
        print(_json.dumps(compacted, indent=2))
        return 0

    print(f"unknown subcommand: {subcmd!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
