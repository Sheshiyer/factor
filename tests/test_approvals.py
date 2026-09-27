"""Tests for scripts/approvals.py

Covers:
  - payload_digest: determinism, sort-key canonicalisation, non-finite rejection
  - make_approval: happy path, expired expiry, path escape, non-finite payload
  - validate_approval: valid record, expired, wrong card/action/target, changed payload,
    missing record, malformed record, non-finite payload, confidence cannot authorize
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVALS_MOD = ROOT / "scripts" / "approvals.py"


def load_approvals():
    spec = importlib.util.spec_from_file_location("approvals", APPROVALS_MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


approvals = load_approvals()


def _future(seconds: int = 3600) -> str:
    return (datetime.now(tz=timezone.utc) + timedelta(seconds=seconds)).isoformat()


def _past(seconds: int = 1) -> str:
    return (datetime.now(tz=timezone.utc) - timedelta(seconds=seconds)).isoformat()


class PayloadDigestTest(unittest.TestCase):
    def test_deterministic_for_same_payload(self):
        d1 = approvals.payload_digest({"action": "send", "page": "about"})
        d2 = approvals.payload_digest({"action": "send", "page": "about"})
        self.assertEqual(d1, d2)

    def test_key_order_does_not_change_digest(self):
        d1 = approvals.payload_digest({"a": 1, "b": 2})
        d2 = approvals.payload_digest({"b": 2, "a": 1})
        self.assertEqual(d1, d2)

    def test_different_payloads_produce_different_digests(self):
        d1 = approvals.payload_digest({"page": "about"})
        d2 = approvals.payload_digest({"page": "contact"})
        self.assertNotEqual(d1, d2)

    def test_digest_is_64_hex_chars(self):
        d = approvals.payload_digest({"x": 1})
        self.assertEqual(len(d), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in d))

    def test_empty_dict_has_a_digest(self):
        d = approvals.payload_digest({})
        self.assertEqual(len(d), 64)

    def test_non_finite_float_raises(self):
        with self.assertRaises(ValueError):
            approvals.payload_digest({"x": math.inf})
        with self.assertRaises(ValueError):
            approvals.payload_digest({"x": -math.inf})
        with self.assertRaises(ValueError):
            approvals.payload_digest({"x": math.nan})

    def test_nested_non_finite_raises(self):
        with self.assertRaises(ValueError):
            approvals.payload_digest({"inner": {"v": math.nan}})

    def test_list_payload_accepted(self):
        d = approvals.payload_digest([1, 2, 3])
        self.assertEqual(len(d), 64)

    def test_list_with_non_finite_raises(self):
        with self.assertRaises(ValueError):
            approvals.payload_digest([1, math.inf, 3])

    def test_none_payload_accepted(self):
        d = approvals.payload_digest(None)
        self.assertEqual(len(d), 64)


class MakeApprovalTest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tmpdir.name) / "company"
        self.root.mkdir()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _make(self, **kwargs):
        defaults = dict(
            root=self.root,
            card_id="card-001",
            action="send",
            target="about.md",
            payload={"page": "about"},
            approver="founder",
            expires_at=_future(),
        )
        defaults.update(kwargs)
        return approvals.make_approval(**defaults)

    def test_happy_path_creates_record_on_disk(self):
        record = self._make()
        self.assertEqual(record["card_id"], "card-001")
        self.assertEqual(record["action"], "send")
        self.assertEqual(record["target"], "about.md")
        self.assertEqual(record["approver"], "founder")
        adir = self.root / "approvals"
        self.assertTrue(adir.is_dir())
        files = list(adir.glob("*.json"))
        self.assertEqual(len(files), 1)
        stored = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(stored["id"], record["id"])

    def test_payload_digest_is_stored(self):
        payload = {"page": "about", "draft": "v1"}
        record = self._make(payload=payload)
        self.assertEqual(record["payload_digest"], approvals.payload_digest(payload))

    def test_expired_expiry_raises(self):
        with self.assertRaises(ValueError):
            self._make(expires_at=_past())

    def test_non_finite_payload_raises(self):
        with self.assertRaises(ValueError):
            self._make(payload={"confidence": math.inf})

    def test_empty_card_id_raises(self):
        with self.assertRaises(ValueError):
            self._make(card_id="")

    def test_empty_action_raises(self):
        with self.assertRaises(ValueError):
            self._make(action="")

    def test_empty_target_raises(self):
        with self.assertRaises(ValueError):
            self._make(target="")

    def test_empty_approver_raises(self):
        with self.assertRaises(ValueError):
            self._make(approver="")

    def test_invalid_expires_at_raises(self):
        with self.assertRaises(ValueError):
            self._make(expires_at="not-a-date")

    def test_path_escape_raises(self):
        with self.assertRaises(ValueError):
            approvals.make_approval(
                root=self.root,
                card_id="../../etc/passwd",
                action="send",
                target="x",
                payload={},
                approver="founder",
                expires_at=_future(),
            )

    def test_two_approvals_for_same_card_and_action_both_stored(self):
        self._make(target="about.md")
        self._make(target="contact.md")
        adir = self.root / "approvals"
        self.assertEqual(len(list(adir.glob("*.json"))), 2)


class ValidateApprovalTest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tmpdir.name) / "company"
        self.root.mkdir()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _make(self, **kwargs):
        defaults = dict(
            root=self.root,
            card_id="card-001",
            action="send",
            target="about.md",
            payload={"page": "about"},
            approver="founder",
            expires_at=_future(),
        )
        defaults.update(kwargs)
        return approvals.make_approval(**defaults)

    def _validate(self, approval, **kwargs):
        defaults = dict(
            root=self.root,
            card_id="card-001",
            action="send",
            target="about.md",
            payload={"page": "about"},
            approval=approval,
        )
        defaults.update(kwargs)
        return approvals.validate_approval(**defaults)

    def test_valid_approval_returns_true(self):
        record = self._make()
        self.assertTrue(self._validate(record))

    def test_valid_approval_id_string_loads_and_validates(self):
        record = self._make()
        self.assertTrue(self._validate(record["id"]))

    def test_expired_approval_returns_false(self):
        record = self._make()
        future_now = datetime.now(tz=timezone.utc) + timedelta(hours=2)
        self.assertFalse(self._validate(record, now=future_now))

    def test_wrong_card_id_returns_false(self):
        record = self._make()
        self.assertFalse(self._validate(record, card_id="card-999"))

    def test_wrong_action_returns_false(self):
        record = self._make()
        self.assertFalse(self._validate(record, action="spend"))

    def test_wrong_target_returns_false(self):
        record = self._make()
        self.assertFalse(self._validate(record, target="other.md"))

    def test_changed_payload_invalidates_approval(self):
        record = self._make()
        self.assertFalse(self._validate(record, payload={"page": "different"}))

    def test_missing_record_id_returns_false(self):
        self.assertFalse(self._validate("nonexistent-id"))

    def test_malformed_json_record_returns_false(self):
        adir = self.root / "approvals"
        adir.mkdir(parents=True, exist_ok=True)
        bad = adir / "bad-id.json"
        bad.write_text("not json", encoding="utf-8")
        self.assertFalse(self._validate("bad-id"))

    def test_missing_required_field_returns_false(self):
        record = self._make()
        del record["approver"]
        self.assertFalse(self._validate(record))

    def test_non_dict_approval_returns_false(self):
        self.assertFalse(self._validate("some-string"))

    def test_non_finite_payload_in_validate_returns_false(self):
        record = self._make()
        self.assertFalse(self._validate(record, payload={"v": math.inf}))

    def test_confidence_cannot_substitute_for_approval(self):
        """A high confidence score is not a valid approval — must be a record."""
        high_confidence = 0.99
        self.assertFalse(
            approvals.validate_approval(
                root=self.root,
                card_id="card-001",
                action="send",
                target="about.md",
                payload={"page": "about"},
                approval=high_confidence,  # type: ignore[arg-type]
            )
        )

    def test_approval_for_different_company_root_returns_false(self):
        """An approval made under one root cannot validate under another root."""
        record = self._make()
        with tempfile.TemporaryDirectory() as tmp2:
            other_root = Path(tmp2) / "other"
            other_root.mkdir()
            result = approvals.validate_approval(
                root=other_root,
                card_id="card-001",
                action="send",
                target="about.md",
                payload={"page": "about"},
                approval=record["id"],
            )
            self.assertFalse(result)

    def test_loaded_dict_is_bound_to_company_and_persisted_record(self):
        record = self._make()
        with tempfile.TemporaryDirectory() as other:
            self.assertFalse(self._validate(record, root=Path(other)))
        forged = dict(record, approver="someone-else")
        self.assertFalse(self._validate(forged))
        (self.root / "approvals" / (record["id"] + ".json")).unlink()
        self.assertFalse(self._validate(record))

    def test_symlinked_store_and_record_fail_closed(self):
        record = self._make()
        path = self.root / "approvals" / (record["id"] + ".json")
        original = path.read_bytes()
        path.unlink()
        outside = self.root.parent / "outside.json"
        outside.write_bytes(original)
        path.symlink_to(outside)
        self.assertFalse(self._validate(record["id"]))
        path.unlink()
        path.parent.rmdir()
        path.parent.symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            self._make()
        self.assertEqual(outside.read_bytes(), original)

    def test_malformed_types_and_naive_clock_fail_closed(self):
        record = self._make()
        self.assertFalse(self._validate(record, now=datetime.now()))
        self.assertFalse(self._validate(record, payload={1: "ambiguous"}))
        self.assertFalse(self._validate(record, payload={"a": object()}))
        self.assertFalse(self._validate("../../outside"))

    def test_spend_and_publish_also_require_explicit_approval(self):
        """send, spend, and publish all require an approval record."""
        for action in ("spend", "publish"):
            with self.subTest(action=action):
                record = self._make(action=action)
                self.assertTrue(self._validate(record, action=action))
                self.assertFalse(self._validate(record, action="send"))


class CLITest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tmpdir.name) / "company"
        self.root.mkdir()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _run(self, args: list):
        import subprocess
        return subprocess.run(
            [sys.executable, str(APPROVALS_MOD)] + args,
            capture_output=True,
            text=True,
        )

    def test_make_and_validate_round_trip(self):
        result = self._run([
            "make",
            str(self.root),
            "card-001",
            "send",
            "about.md",
            "founder",
            _future(),
            "--payload-json", json.dumps({"page": "about"}),
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(result.stdout)
        approval_id = record["id"]

        result2 = self._run([
            "validate",
            str(self.root),
            "card-001",
            "send",
            "about.md",
            approval_id,
            "--payload-json", json.dumps({"page": "about"}),
        ])
        self.assertEqual(result2.returncode, 0, result2.stderr)
        self.assertIn("valid", result2.stdout)

    def test_validate_changed_payload_exits_1(self):
        result = self._run([
            "make",
            str(self.root),
            "card-001",
            "send",
            "about.md",
            "founder",
            _future(),
            "--payload-json", json.dumps({"page": "about"}),
        ])
        approval_id = json.loads(result.stdout)["id"]
        result2 = self._run([
            "validate",
            str(self.root),
            "card-001",
            "send",
            "about.md",
            approval_id,
            "--payload-json", json.dumps({"page": "DIFFERENT"}),
        ])
        self.assertEqual(result2.returncode, 1)
        self.assertIn("invalid", result2.stdout)

    def test_list_shows_records(self):
        self._run([
            "make", str(self.root), "card-001", "send", "about.md", "founder", _future(),
        ])
        result = self._run(["list", str(self.root)])
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["card_id"], "card-001")

    def test_make_expired_exits_1(self):
        result = self._run([
            "make", str(self.root), "card-001", "send", "about.md", "founder", _past(),
        ])
        self.assertEqual(result.returncode, 1)

    def test_no_subcommand_exits_2(self):
        result = self._run([])
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
