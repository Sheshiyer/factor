import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import knowledge
import corrections
import content_trial


class ContentTrialTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "company"
        (self.root / "wiki").mkdir(parents=True)
        (self.root / "wiki/index.md").write_text("[Voice](voice.md)\n")
        (self.root / "wiki/voice.md").write_text("# Voice\nKeep this page.\n")
        self.revision = knowledge.import_source(self.root, {
            "id": "source", "url": "https://example.test/report", "author": "Founder",
            "published_at": None, "body": "Our product has three rooms.",
            "completeness": "complete"})
        knowledge.add_claim(self.root, {"id": "rooms", "subject": "product",
            "predicate": "room count", "statement": "Our product has three rooms.",
            "source_id": "source", "source_revision": self.revision,
            "locator": "paragraph 1", "effective_at": None, "page": "voice.md"})
        self.text = "Amazing product. [Amazing source](https://example.test/Amazing)\n"

    def packet(self, receipt):
        return json.loads(Path(receipt["path"]).read_text())["packet"]

    def trial(self, **kwargs):
        return content_trial.run_trial(self.root, "voice.md", self.text, "card-1", **kwargs)

    def accept_claim(self):
        knowledge.review_claim(self.root, "rooms", "accepted")

    def test_full_review_correction_replay_and_dedup(self):
        blocked = self.trial()
        self.assertEqual(blocked["status"], "blocked")
        self.assertIsNone(self.packet(blocked)["draft"])
        self.accept_claim()
        first = self.trial()
        self.assertEqual(self.packet(first)["draft"], self.text)
        self.assertEqual(self.packet(first)["claims"][0]["source_revision"], self.revision)
        before = Path(first["path"]).stat().st_mtime_ns
        repeated = self.trial()
        self.assertTrue(repeated["deduplicated"])
        self.assertEqual(repeated["path"], first["path"])
        self.assertEqual(Path(first["path"]).stat().st_mtime_ns, before)
        for number in (1, 2):
            corrections.record_correction(self.root, {
                "original": "Amazing", "rewrite": "Useful", "reason": "Avoid hype",
                "scope": "voice.md", "example": f"Amazing example {number}",
                "regression_example": f"Amazing example {number}"})
        proposal = corrections.propose_rule(self.root, "voice.md", "Avoid hype")
        self.assertEqual(self.packet(self.trial())["draft"], self.text)
        expected = hashlib.sha256((self.root / "wiki/voice.md").read_bytes()).hexdigest()
        corrections.accept_rule(self.root, proposal, "Founder", expected)
        next_draft = self.trial()
        self.assertNotEqual(next_draft["output_sha256"], first["output_sha256"])
        self.assertEqual(self.packet(next_draft)["draft"],
                         "Useful product. [Amazing source](https://example.test/Amazing)\n")
        self.assertTrue(self.trial()["deduplicated"])
        self.assertFalse(self.packet(next_draft)["published"])
        self.assertEqual(self.packet(next_draft)["external_actions"], [])
        stored = json.loads(Path(next_draft["path"]).read_text())
        self.assertEqual(content_trial.digest(stored["packet"]), stored["output_sha256"])

    def test_conflicting_claims_and_stale_source_block(self):
        self.accept_claim()
        knowledge.add_claim(self.root, {"id": "other", "subject": "product",
            "predicate": "room count", "statement": "Our product has five rooms.",
            "source_id": "source", "source_revision": self.revision,
            "locator": "paragraph 2", "page": "voice.md"})
        knowledge.review_claim(self.root, "other", "accepted")
        receipt = self.trial()
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(self.packet(receipt)["conflicts"])
        knowledge.review_claim(self.root, "other", "rejected")
        knowledge.import_source(self.root, {"id": "source", "url": "https://example.test/report",
                                           "body": "New version.", "completeness": "complete"})
        self.assertEqual(self.trial()["status"], "blocked")

    def test_missing_body_blocks(self):
        revision = knowledge.import_source(self.root, {"id": "missing", "body": None,
                                                      "completeness": "missing"})
        knowledge.add_claim(self.root, {"id": "missing", "subject": "missing",
            "predicate": "content", "statement": "Unavailable", "source_id": "missing",
            "source_revision": revision, "locator": "unknown", "page": "voice.md"})
        knowledge.review_claim(self.root, "missing", "accepted")
        receipt = self.trial()
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(self.packet(receipt)["gaps"])

    def test_output_and_page_path_boundaries(self):
        self.accept_claim()
        for output in ("../elsewhere", "/tmp/factor-unwanted", "wiki/packets", "output/../wiki"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                self.trial(output_dir=output)
        (self.root / "output").symlink_to(Path(self.temp.name), target_is_directory=True)
        with self.assertRaises(ValueError):
            self.trial()
        (self.root / "output").unlink()
        (self.root / "wiki/escape.md").symlink_to(self.root / "wiki/voice.md")
        with self.assertRaises(ValueError):
            self.trial()

    def test_explicit_root_symlink_and_missing_revision_evidence(self):
        alias = Path(self.temp.name) / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "root must not be a symlink"):
            content_trial.run_trial(alias, "voice.md", self.text, "card-1")
        self.accept_claim()
        evidence = knowledge.retrieve(self.root, "voice.md")
        evidence["sources"] = {}
        with patch.object(knowledge, "retrieve", return_value=evidence):
            result = self.trial()
        self.assertEqual(result["status"], "blocked")
        self.assertIn("claim source revision evidence is missing", self.packet(result)["blockers"])

    def test_unindexed_page_is_not_allowed(self):
        (self.root / "wiki/private.md").write_text("Private")
        with self.assertRaises(ValueError):
            content_trial.run_trial(self.root, "private.md", self.text, "card-1")

    def test_corrupted_existing_packet_is_not_silently_reused(self):
        self.accept_claim()
        first = self.trial()
        Path(first["path"]).write_text("tampered")
        with self.assertRaisesRegex(ValueError, "modified"):
            self.trial()

    def test_same_input_with_changed_actual_output_is_not_deduplicated(self):
        self.accept_claim()
        first = self.trial()
        with patch.object(corrections, "apply_corrections", side_effect=lambda root, page, text: text.replace("Amazing", "Useful")):
            changed = self.trial()
        self.assertEqual(first["input_sha256"], changed["input_sha256"])
        self.assertNotEqual(first["output_sha256"], changed["output_sha256"])
        self.assertFalse(changed["deduplicated"])

    def test_protected_citations_are_unchanged(self):
        text = "Amazing [Amazing][ref] [[Amazing]] [^Amazing]\n[ref]: https://example.test/Amazing\n[Amazing\nsource](https://example.test/nested(Amazing) \"Amazing title\")\n"
        with patch.object(corrections, "apply_corrections", side_effect=lambda root, page, text: text.replace("Amazing", "Useful")):
            result = content_trial.corrected_prose(self.root, "voice.md", text)
        self.assertEqual(result, text.replace("Amazing", "Useful", 1))


if __name__ == "__main__":
    unittest.main()
