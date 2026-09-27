#!/usr/bin/env python3
"""Approval primitives for exact-action gating.

Trusted caller boundary
-----------------------
This module validates *local* approval records stored beneath a company root.
It does not implement authenticated external transport, one-time consumption,
or any external adapter.  The caller is responsible for:

  - Confirming the approver identity matches the company's founder record.
  - Ensuring the approval record is consumed (deleted or marked used) before
    triggering the external action.  Replay protection is deferred.
  - Never treating a confidence score, however high, as a substitute for an
    explicit approval record.  A score of 0.99 cannot authorize a send,
    spend, or publish.

A changed payload, scope, or target invalidates the approval.  The digest
function is deterministic and canonical: the same logical payload always
produces the same digest.

Public API
----------
    payload_digest(payload) -> str
    make_approval(root, card_id, action, target, payload, approver, expires_at) -> dict
    validate_approval(root, card_id, action, target, payload, approval, now=None) -> bool

CLI
---
    approvals.py make   <root> <card_id> <action> <target> <approver> <expires_at> [--payload-json <json>]
    approvals.py validate <root> <card_id> <action> <target> <approval_id> [--payload-json <json>]
    approvals.py list   <root>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tempfile
import uuid
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

APPROVALS_DIR = "approvals"


def _safe_root(root: Path) -> Path:
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("company root must be an existing directory, not a symlink")
    return root.resolve()


def _approvals_dir(root: Path) -> Path:
    path = _safe_root(root) / APPROVALS_DIR
    if path.is_symlink():
        raise ValueError("approvals directory cannot be a symlink")
    return path


def _check_within_root(root: Path, path: Path) -> None:
    """Raise ValueError if path is outside root (traversal / symlink escape)."""
    safe_root = _safe_root(root)
    if path.is_symlink():
        raise ValueError("approval file cannot be a symlink")
    try:
        path.resolve().relative_to(safe_root)
    except ValueError:
        raise ValueError(f"path escape: {path} is outside {safe_root}")


# ---------------------------------------------------------------------------
# Payload canonicalisation and digest
# ---------------------------------------------------------------------------


def _canonical_json(payload: Any) -> bytes:
    """Return a stable, sorted JSON encoding of *payload*."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def _assert_finite_payload(payload: Any) -> None:
    """Raise ValueError if payload contains non-finite floats."""
    if isinstance(payload, float):
        if not math.isfinite(payload):
            raise ValueError(f"non-finite value in payload: {payload!r}")
    elif isinstance(payload, dict):
        for v in payload.values():
            _assert_finite_payload(v)
    elif isinstance(payload, (list, tuple)):
        for v in payload:
            _assert_finite_payload(v)


def payload_digest(payload: Any) -> str:
    """Return a hex SHA-256 digest of the canonical JSON representation of *payload*.

    Non-finite floats (inf, -inf, nan) are rejected because they have no
    canonical JSON representation.
    """
    def check(value):
        if value is None or type(value) in (str, bool, int):
            return
        if type(value) is float and math.isfinite(value):
            return
        if type(value) is list:
            for child in value: check(child)
            return
        if type(value) is dict and all(type(key) is str for key in value):
            for child in value.values(): check(child)
            return
        raise ValueError("payload must contain finite JSON values and string object keys")
    check(payload)
    raw = _canonical_json(payload)
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# Approval record structure
# ---------------------------------------------------------------------------


def _now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def _parse_iso(dt_str: str) -> datetime:
    """Parse an ISO-8601 string with timezone.  Raise ValueError on failure."""
    try:
        # Python 3.11+ fromisoformat handles Z; older versions need normalisation.
        normalised = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(normalised)
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"invalid datetime: {dt_str!r}") from exc


# ---------------------------------------------------------------------------
# make_approval
# ---------------------------------------------------------------------------


def make_approval(
    root: Path,
    card_id: str,
    action: str,
    target: str,
    payload: Any,
    approver: str,
    expires_at: str,
) -> dict:
    """Create and persist an approval record beneath *root/approvals/*.

    Parameters
    ----------
    root:        Company root directory.
    card_id:     Identifier of the card authorising this action.
    action:      One of "send", "spend", "publish" (or a future gated action).
    target:      Target identifier (e.g. file path, endpoint slug, card name).
    payload:     Canonical payload to be approved.  Must contain only finite numbers.
    approver:    Approver identifier (e.g. founder name or "founder").
    expires_at:  ISO-8601 expiry timestamp (must be in the future when called).

    Returns the persisted approval dict.  Raises ValueError for invalid inputs.
    """
    if not card_id or not isinstance(card_id, str):
        raise ValueError("card_id must be a non-empty string")
    if not action or not isinstance(action, str):
        raise ValueError("action must be a non-empty string")
    if not target or not isinstance(target, str):
        raise ValueError("target must be a non-empty string")
    if not approver or not isinstance(approver, str):
        raise ValueError("approver must be a non-empty string")

    if not re.fullmatch(r"[A-Za-z0-9_.-]+", card_id) or card_id in (".", ".."):
        raise ValueError("invalid card_id")
    if action not in {"send", "spend", "publish"}:
        raise ValueError("unsupported action")
    if not target.strip() or not approver.strip():
        raise ValueError("target and approver cannot be whitespace")
    expires_dt = _parse_iso(expires_at)
    now = _now_utc()
    if expires_dt.tzinfo is None:
        raise ValueError("expires_at must include timezone")
    if expires_dt <= now:
        raise ValueError(f"expires_at {expires_at!r} is already in the past")

    digest = payload_digest(payload)

    approval_id = uuid.uuid4().hex

    record = {
        "id": approval_id,
        "company_root": str(_safe_root(root)),
        "card_id": card_id,
        "action": action,
        "target": target,
        "payload_digest": digest,
        "approver": approver,
        "approved_at": now.isoformat(),
        "expires_at": expires_dt.isoformat(),
    }

    approvals_path = _approvals_dir(root)
    _check_within_root(root, approvals_path)
    approvals_path.mkdir(parents=True, exist_ok=True)

    record_path = approvals_path / f"{approval_id}.json"
    _check_within_root(root, record_path)

    # Atomic write
    fd, tmp_name = tempfile.mkstemp(prefix=".approval-", dir=approvals_path)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(record, indent=2) + "\n")
        _check_within_root(root, record_path)
        tmp.replace(record_path)
    finally:
        tmp.unlink(missing_ok=True)

    return record


# ---------------------------------------------------------------------------
# validate_approval
# ---------------------------------------------------------------------------


def validate_approval(
    root: Path,
    card_id: str,
    action: str,
    target: str,
    payload: Any,
    approval: dict | str,
    now: datetime | None = None,
) -> bool:
    """Return True only if *approval* is a valid, unexpired, matching approval.

    Accepts either a loaded approval dict or an approval_id string.  When an
    ID string is supplied, the corresponding record is loaded from disk.

    Rejects:
      - Malformed or missing records.
      - Expired records (expires_at <= now).
      - Records whose card_id, action, or target do not match.
      - Records whose payload_digest does not match payload_digest(payload).
      - Non-finite payload values.

    A confidence argument is not accepted.  High confidence cannot replace
    an explicit approval record.
    """
    try:
        now = _now_utc() if now is None else now
        if not isinstance(now, datetime) or now.tzinfo is None:
            return False
        root_id = str(_safe_root(root))
        if isinstance(approval, dict):
            supplied = approval
            approval_id = supplied.get("id")
        elif isinstance(approval, str):
            supplied = None
            approval_id = approval
        else:
            return False
        if not isinstance(approval_id, str) or not re.fullmatch(r"[a-f0-9]{32}", approval_id):
            return False
        record_path = _approvals_dir(root) / f"{approval_id}.json"
        _check_within_root(root, record_path)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or (supplied is not None and supplied != record):
            return False
        fields = ("id", "company_root", "card_id", "action", "target", "payload_digest", "approver", "approved_at", "expires_at")
        if any(not isinstance(record.get(key), str) or not record[key].strip() for key in fields):
            return False
        if record["id"] != approval_id or record["company_root"] != root_id:
            return False
        expires = _parse_iso(record["expires_at"])
        issued = _parse_iso(record["approved_at"])
        if expires.tzinfo is None or issued.tzinfo is None or not issued <= now < expires:
            return False
        return (action in {"send", "spend", "publish"}
                and record["card_id"] == card_id
                and record["action"] == action
                and record["target"] == target
                and record["payload_digest"] == payload_digest(payload))
    except (ValueError, TypeError, AttributeError, OSError, RecursionError):
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _cmd_make(args: argparse.Namespace) -> int:
    root = Path(args.root)
    payload: Any = {}
    if args.payload_json:
        try:
            payload = json.loads(args.payload_json)
        except json.JSONDecodeError as exc:
            print(f"invalid payload JSON: {exc}", file=sys.stderr)
            return 2
    try:
        record = make_approval(
            root=root,
            card_id=args.card_id,
            action=args.action,
            target=args.target,
            payload=payload,
            approver=args.approver,
            expires_at=args.expires_at,
        )
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(record, indent=2))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.root)
    payload: Any = {}
    if args.payload_json:
        try:
            payload = json.loads(args.payload_json)
        except json.JSONDecodeError as exc:
            print(f"invalid payload JSON: {exc}", file=sys.stderr)
            return 2
    ok = validate_approval(
        root=root,
        card_id=args.card_id,
        action=args.action,
        target=args.target,
        payload=payload,
        approval=args.approval_id,
    )
    print("valid" if ok else "invalid")
    return 0 if ok else 1


def _cmd_list(args: argparse.Namespace) -> int:
    root = Path(args.root)
    try:
        adir = _approvals_dir(root)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not adir.is_dir():
        print("no approvals")
        return 0
    records = []
    for path in sorted(adir.glob("*.json")):
        try:
            _check_within_root(root, path)
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass
    print(json.dumps(records, indent=2))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Approval primitives")
    sub = parser.add_subparsers(dest="command")

    p_make = sub.add_parser("make", help="create an approval record")
    p_make.add_argument("root")
    p_make.add_argument("card_id")
    p_make.add_argument("action")
    p_make.add_argument("target")
    p_make.add_argument("approver")
    p_make.add_argument("expires_at")
    p_make.add_argument("--payload-json", default="")

    p_val = sub.add_parser("validate", help="validate an approval record")
    p_val.add_argument("root")
    p_val.add_argument("card_id")
    p_val.add_argument("action")
    p_val.add_argument("target")
    p_val.add_argument("approval_id")
    p_val.add_argument("--payload-json", default="")

    p_list = sub.add_parser("list", help="list all approval records")
    p_list.add_argument("root")

    args = parser.parse_args(argv[1:])
    if args.command == "make":
        return _cmd_make(args)
    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "list":
        return _cmd_list(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
