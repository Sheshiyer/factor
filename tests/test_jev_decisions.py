"""Tests for scripts/jev_decisions.py

Covers behavior and failure boundaries for:
- validate_decision
- compact_context
- CLI subcommands
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JEV = ROOT / "scripts" / "jev_decisions.py"


def load_jev():
    spec = importlib.util.spec_from_file_location("jev_decisions", JEV)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ValidateDecisionTest(unittest.TestCase):
    def setUp(self):
        self.mod = load_jev()

    # --- accepted real results ---

    def test_accepted_real_result(self):
        candidates = ["opt-a", "opt-b"]
        result = {
            "outcome": "opt-a",
            "confidence": 0.9,
            "provider": "acme-ai",
            "model": "model-v1",
        }
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_ACCEPTED)
        self.assertEqual(status["outcome"], "opt-a")
        self.assertEqual(status["confidence"], 0.9)
        self.assertFalse(status["synthetic"])

    def test_accepted_at_exact_min_confidence(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.5, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result, min_confidence=0.5)
        self.assertEqual(status["status"], self.mod.STATUS_ACCEPTED)

    def test_accepted_confidence_1_0(self):
        candidates = ["x"]
        result = {"outcome": "x", "confidence": 1.0, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_ACCEPTED)

    def test_accepted_confidence_0_0_with_zero_min(self):
        candidates = ["x"]
        result = {"outcome": "x", "confidence": 0.0, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result, min_confidence=0.0)
        self.assertEqual(status["status"], self.mod.STATUS_ACCEPTED)

    # --- low confidence ---

    def test_low_confidence_real_result(self):
        candidates = ["opt-a"]
        result = {"outcome": "opt-a", "confidence": 0.3, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result, min_confidence=0.5)
        self.assertEqual(status["status"], self.mod.STATUS_LOW_CONFIDENCE)
        self.assertIn("0.3", status["reason"])

    def test_low_confidence_custom_min(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.6, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result, min_confidence=0.8)
        self.assertEqual(status["status"], self.mod.STATUS_LOW_CONFIDENCE)

    # --- invalid confidence ---

    def test_confidence_missing(self):
        candidates = ["a"]
        result = {"outcome": "a", "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    def test_confidence_none(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": None, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    def test_confidence_nan(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": float("nan"), "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)
        self.assertIn("finite", status["reason"])

    def test_confidence_inf(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": float("inf"), "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    def test_confidence_above_1(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 1.1, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    def test_confidence_below_0(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": -0.1, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    def test_confidence_string_is_invalid(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": "high", "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CONFIDENCE)

    # --- invalid candidate ---

    def test_outcome_not_in_candidates(self):
        candidates = ["opt-a", "opt-b"]
        result = {"outcome": "opt-c", "confidence": 0.8, "provider": "p", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CANDIDATE)
        self.assertIn("opt-c", status["reason"])

    def test_empty_candidates_list(self):
        result = {"outcome": "opt-a", "confidence": 0.9, "provider": "p", "model": "m"}
        status = self.mod.validate_decision([], result)
        self.assertEqual(status["status"], self.mod.STATUS_INVALID_CANDIDATE)

    # --- missing receipt ---

    def test_missing_provider_field(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.9, "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_MISSING_RECEIPT)
        self.assertIn("provider", status["reason"])

    def test_missing_model_field(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.9, "provider": "p"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_MISSING_RECEIPT)
        self.assertIn("model", status["reason"])

    def test_empty_provider_is_missing(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.9, "provider": "", "model": "m"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_MISSING_RECEIPT)

    # --- non-decision outcomes ---

    def test_abstain_outcome(self):
        candidates = ["a", "b"]
        result = {"outcome": "abstain", "confidence": 0.0}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_ABSTAINED)

    def test_abstained_outcome(self):
        candidates = ["a"]
        result = {"outcome": "abstained"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_ABSTAINED)

    def test_disabled_outcome(self):
        candidates = ["a"]
        result = {"outcome": "disabled"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_DISABLED)

    def test_unavailable_outcome(self):
        candidates = ["a"]
        result = {"outcome": "unavailable"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_UNAVAILABLE)

    def test_timeout_outcome(self):
        candidates = ["a"]
        result = {"outcome": "timeout"}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_TIMEOUT)

    def test_none_outcome_is_abstained(self):
        candidates = ["a"]
        result = {"outcome": None}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_ABSTAINED)

    # --- synthetic ---

    def test_synthetic_label_accepted(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.7, "synthetic": True}
        status = self.mod.validate_decision(candidates, result)
        self.assertEqual(status["status"], self.mod.STATUS_SYNTHETIC)
        self.assertTrue(status["synthetic"])

    def test_synthetic_does_not_require_provider_model(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.8, "synthetic": True}
        status = self.mod.validate_decision(candidates, result)
        # Should not be STATUS_MISSING_RECEIPT
        self.assertNotEqual(status["status"], self.mod.STATUS_MISSING_RECEIPT)

    def test_synthetic_low_confidence(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.2, "synthetic": True}
        status = self.mod.validate_decision(candidates, result, min_confidence=0.5)
        self.assertEqual(status["status"], self.mod.STATUS_LOW_CONFIDENCE)

    def test_synthetic_reason_never_implies_provider_call(self):
        candidates = ["a"]
        result = {"outcome": "a", "confidence": 0.9, "synthetic": True}
        status = self.mod.validate_decision(candidates, result)
        self.assertIn("synthetic", status["reason"])
        self.assertIn("no provider call", status["reason"])

    # --- shadow_only pass-through ---

    def test_shadow_only_is_passed_through(self):
        candidates = ["a"]
        result = {
            "outcome": "a", "confidence": 0.9,
            "provider": "p", "model": "m",
            "shadow_only": True
        }
        status = self.mod.validate_decision(candidates, result)
        self.assertTrue(status["shadow_only"])

    # --- status dict completeness ---

    def test_status_dict_always_has_required_keys(self):
        required = {"status", "outcome", "confidence", "synthetic", "shadow_only", "reason"}
        for result in [
            {"outcome": "a", "confidence": 0.9, "provider": "p", "model": "m"},
            {"outcome": "abstain"},
            {"outcome": "bad", "confidence": 0.9, "provider": "p", "model": "m"},
        ]:
            status = self.mod.validate_decision(["a"], result)
            self.assertTrue(required.issubset(status.keys()), f"missing keys in {status!r}")


class CompactContextTest(unittest.TestCase):
    def setUp(self):
        self.mod = load_jev()

    def _msg(self, msg_id: str, role: str, content: str) -> dict:
        return {"id": msg_id, "role": role, "content": content}

    # --- ranking_ok=False: full fallback ---

    def test_ranking_fail_returns_all_messages(self):
        msgs = [
            self._msg("1", "user", "first"),
            self._msg("2", "assistant", "second"),
            self._msg("3", "user", "third"),
        ]
        result = self.mod.compact_context(msgs, [], ranking_ok=False)
        self.assertEqual(result, msgs)

    def test_ranking_fail_preserves_original_references(self):
        msgs = [self._msg("1", "user", "hello")]
        result = self.mod.compact_context(msgs, [], ranking_ok=False)
        self.assertIs(result[0], msgs[0])

    # --- keep_ids respected when ranking_ok=True ---

    def test_keep_ids_retained(self):
        msgs = [
            self._msg("k1", "user", "keep this"),
            self._msg("d1", "user", "drop this"),
            self._msg("k2", "assistant", "also keep"),
        ]
        result = self.mod.compact_context(msgs, ["k1", "k2"], ranking_ok=True)
        ids = [m["id"] for m in result]
        self.assertIn("k1", ids)
        self.assertIn("k2", ids)
        self.assertNotIn("d1", ids)

    def test_keep_ids_preserve_original_dict(self):
        msg = self._msg("k1", "user", "important")
        result = self.mod.compact_context([msg], ["k1"], ranking_ok=True)
        self.assertIs(result[0], msg)

    # --- protected messages always kept ---

    def test_system_role_always_kept(self):
        msgs = [
            self._msg("s1", "system", "system instructions"),
            self._msg("u1", "user", "drop me"),
        ]
        result = self.mod.compact_context(msgs, [], ranking_ok=True)
        ids = [m["id"] for m in result]
        self.assertIn("s1", ids)
        self.assertNotIn("u1", ids)

    def test_do_not_marker_protected(self):
        msg = self._msg("p1", "user", "Do not send emails")
        other = self._msg("d1", "user", "ordinary message")
        result = self.mod.compact_context([msg, other], [], ranking_ok=True)
        ids = [m["id"] for m in result]
        self.assertIn("p1", ids)
        self.assertNotIn("d1", ids)

    def test_must_not_marker_protected(self):
        msg = self._msg("p1", "assistant", "You must not publish this")
        result = self.mod.compact_context([msg], [], ranking_ok=True)
        self.assertIn("p1", [m["id"] for m in result])

    def test_prohibited_marker_protected(self):
        msg = self._msg("p1", "user", "This action is prohibited")
        result = self.mod.compact_context([msg], [], ranking_ok=True)
        self.assertIn("p1", [m["id"] for m in result])

    def test_commitment_marker_protected(self):
        msg = self._msg("c1", "user", "My commitment is to deliver")
        result = self.mod.compact_context([msg], [], ranking_ok=True)
        self.assertIn("c1", [m["id"] for m in result])

    def test_unresolved_question_protected(self):
        msg = self._msg("q1", "user", "unresolved question: what to do?")
        result = self.mod.compact_context([msg], [], ranking_ok=True)
        self.assertIn("q1", [m["id"] for m in result])

    def test_path_marker_protected(self):
        msg = self._msg("p1", "user", "Path: /some/important/path")
        result = self.mod.compact_context([msg], [], ranking_ok=True)
        self.assertIn("p1", [m["id"] for m in result])

    # --- order preserved ---

    def test_order_preserved_after_compaction(self):
        msgs = [
            self._msg("a", "system", "sys"),
            self._msg("b", "user", "drop"),
            self._msg("c", "user", "keep"),
        ]
        result = self.mod.compact_context(msgs, ["c"], ranking_ok=True)
        ids = [m["id"] for m in result]
        # "a" (system) and "c" (keep_id) must both appear in order
        self.assertLess(ids.index("a"), ids.index("c"))

    # --- empty and edge cases ---

    def test_empty_messages_returns_empty(self):
        result = self.mod.compact_context([], [], ranking_ok=True)
        self.assertEqual(result, [])

    def test_all_droppable_messages_returns_original_as_safety_net(self):
        msgs = [
            self._msg("x", "user", "nothing special"),
        ]
        result = self.mod.compact_context(msgs, [], ranking_ok=True)
        # Safety net: if compaction would drop everything, return original
        self.assertEqual(result, msgs)

    def test_no_id_messages_handled(self):
        msgs = [
            {"role": "user", "content": "no id here"},
            {"role": "system", "content": "system message"},
        ]
        result = self.mod.compact_context(msgs, [], ranking_ok=True)
        # System message kept; no-id user message dropped (not in keep_ids)
        roles_kept = [m["role"] for m in result]
        self.assertIn("system", roles_kept)

    def test_keep_id_not_in_messages_ignored_gracefully(self):
        msgs = [self._msg("a", "user", "nothing to keep")]
        # keep_id "ghost" doesn't exist in messages — should not crash
        result = self.mod.compact_context(msgs, ["ghost"], ranking_ok=True)
        # "a" is not system and not in keep_ids, ghost doesn't exist
        # Safety net: result is original since nothing survives
        self.assertIsInstance(result, list)


class CLIJevTest(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(JEV)] + list(args),
            capture_output=True,
            text=True,
        )

    def test_validate_decision_accepted(self):
        result_json = json.dumps({
            "outcome": "opt-a",
            "confidence": 0.9,
            "provider": "acme",
            "model": "v1",
        })
        result = self._run("validate-decision", result_json, "opt-a,opt-b")
        self.assertEqual(result.returncode, 0, result.stderr)
        status = json.loads(result.stdout)
        self.assertEqual(status["status"], "accepted")

    def test_validate_decision_low_confidence(self):
        result_json = json.dumps({
            "outcome": "opt-a",
            "confidence": 0.2,
            "provider": "p",
            "model": "m",
        })
        result = self._run("validate-decision", result_json, "opt-a")
        self.assertEqual(result.returncode, 0, result.stderr)
        status = json.loads(result.stdout)
        self.assertEqual(status["status"], "low_confidence")

    def test_compact_context_ranking_ok(self):
        msgs = json.dumps([
            {"id": "k1", "role": "user", "content": "keep"},
            {"id": "d1", "role": "user", "content": "drop"},
        ])
        result = self._run("compact-context", msgs, "k1", "ranking_ok")
        self.assertEqual(result.returncode, 0, result.stderr)
        compacted = json.loads(result.stdout)
        ids = [m["id"] for m in compacted]
        self.assertIn("k1", ids)
        self.assertNotIn("d1", ids)

    def test_compact_context_ranking_fail_preserves_all(self):
        msgs = json.dumps([
            {"id": "a", "role": "user", "content": "one"},
            {"id": "b", "role": "user", "content": "two"},
        ])
        result = self._run("compact-context", msgs, "", "ranking_fail")
        self.assertEqual(result.returncode, 0, result.stderr)
        compacted = json.loads(result.stdout)
        self.assertEqual(len(compacted), 2)

    def test_no_args_exits_2(self):
        result = self._run()
        self.assertEqual(result.returncode, 2)

    def test_unknown_subcommand_exits_2(self):
        result = self._run("frobnicate")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()

class HardenedBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_jev()

    def test_malformed_results_fail_closed(self):
        for result in (None, [], {'outcome': []}, {'outcome': 'a', 'confidence': True}, {'outcome':'a','confidence':.9,'synthetic':'false'}, {'outcome':'a','confidence':.9,'provider':[], 'model':'m'}):
            status = self.mod.validate_decision(['a'], result)
            self.assertNotIn(status['status'], ('accepted', 'synthetic'))
        for threshold in (float('nan'), float('inf'), True, '0.5', -1):
            status=self.mod.validate_decision(['a'], {'outcome':'a','confidence':.9,'synthetic':True}, threshold)
            self.assertEqual(status['status'], 'invalid_confidence')

    def test_shadow_is_always_explicit(self):
        result = self.mod.validate_decision(['a'], {'outcome':'a','confidence':.9,'provider':'p','model':'m'})
        self.assertEqual(result['status'],'accepted')
        self.assertIs(result['shadow_only'], True)

    def test_invalid_ranking_keeps_original_objects(self):
        messages=[{'id':'a','content':'ordinary'}, {'id':'b','content':'other'}]
        for keep, flag in ((['missing'],True), (['a'],'false'), ([[]],True)):
            output=self.mod.compact_context(messages,keep,flag)
            self.assertEqual(output,messages)
            self.assertIs(output[0],messages[0])

    def test_protected_structured_context_and_exact_entries(self):
        messages=[{'id':'dev','role':'developer','content':'instruction'}, {'id':'path','content':'/tmp/company'}, {'id':'question','content':'When?'}, {'id':'commit','commitment':True,'content':'promised'}, {'id':'kept','content':' bytes\r\n'}, {'id':'drop','content':'noise'}]
        output=self.mod.compact_context(messages,['kept'],True)
        self.assertEqual(output,messages[:-1])
        for index, item in enumerate(output): self.assertIs(item,messages[index])

    def test_missing_outcome_and_reserved_candidates(self):
        self.assertEqual(self.mod.validate_decision(['a'],{})['status'],'invalid_result')
        self.assertEqual(self.mod.validate_decision(['a'],{'outcome':None})['status'],'abstained')
        self.assertEqual(self.mod.validate_decision(['timeout'],{'outcome':'timeout'})['status'],'invalid_candidate')
