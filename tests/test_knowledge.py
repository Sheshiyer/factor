"""Tests for scripts/knowledge.py — Worker A.

Covers:
- import_source: idempotent, revision digest, null body, new revision
- add_claim: stores correctly, rejects unknown source, rejects wrong revision
- review_claim: updates status, rejects invalid status, rejects unknown claim
- retrieve: returns accepted claims, gaps, conflicts, source evidence
- retrieve: rejects traversal, symlinks, unindexed pages
- CLI subcommands end-to-end
- Atomic write (temp file replaced)
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "scripts" / "knowledge.py"


def load_knowledge():
    spec = importlib.util.spec_from_file_location("factor_knowledge", KNOWLEDGE)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


K = load_knowledge()


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(KNOWLEDGE)] + list(args),
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_source(source_id: str = "src-1", body: str | None = "Article body.") -> dict:
    return {
        "id": source_id,
        "url": "https://example.com/article",
        "author": "A. Writer",
        "published_at": "2026-09-01",
        "body": body,
        "completeness": "complete" if body else "missing",
    }


def _make_claim(
    claim_id: str,
    source_id: str,
    source_revision: str,
    page: str = "topic.md",
    subject: str = "Factor",
    predicate: str = "version",
    statement: str = "0.5.0",
) -> dict:
    return {
        "id": claim_id,
        "subject": subject,
        "predicate": predicate,
        "statement": statement,
        "source_id": source_id,
        "source_revision": source_revision,
        "locator": "§ Introduction",
        "effective_at": "2026-09-01",
        "page": page,
    }


# ---------------------------------------------------------------------------
# import_source
# ---------------------------------------------------------------------------

class TestImportSource(unittest.TestCase):

    def test_returns_hex_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            digest = K.import_source(root, _make_source())
            self.assertIsInstance(digest, str)
            self.assertEqual(len(digest), 64)  # SHA-256 hex

    def test_idempotent_same_id_and_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d1 = K.import_source(root, _make_source())
            d2 = K.import_source(root, _make_source())
            self.assertEqual(d1, d2)
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertEqual(len(store["sources"]), 1)

    def test_new_revision_on_changed_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d1 = K.import_source(root, _make_source(body="Original"))
            d2 = K.import_source(root, _make_source(body="Updated content"))
            self.assertNotEqual(d1, d2)
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            src = store["sources"]["src-1"]
            self.assertEqual(src["revision"], d2)
            self.assertEqual(src.get("prior_revision"), d1)

    def test_null_body_completeness_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = _make_source(body=None)
            record["completeness"] = "missing"
            digest = K.import_source(root, record)
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            src = store["sources"]["src-1"]
            self.assertIsNone(src["body"])
            self.assertEqual(src["completeness"], "missing")
            self.assertEqual(src["revision"], digest)

    def test_requires_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                K.import_source(root, {"url": "https://example.com"})

    def test_identical_content_hash_independent_of_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d1 = K.import_source(root, _make_source("src-a"))
            d2 = K.import_source(root, _make_source("src-b"))
            self.assertEqual(d1, d2)
            self.assertEqual(d1, hashlib.sha256(b"Article body.").hexdigest())

    def test_writes_wiki_knowledge_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            K.import_source(root, _make_source())
            path = root / "wiki" / "knowledge.json"
            self.assertTrue(path.is_file())
            data = json.loads(path.read_text())
            self.assertIn("sources", data)
            self.assertIn("claims", data)

    def test_atomic_no_partial_file(self):
        """knowledge.json.new must not be left behind."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            K.import_source(root, _make_source())
            self.assertFalse((root / "wiki" / "knowledge.json.new").exists())


# ---------------------------------------------------------------------------
# add_claim
# ---------------------------------------------------------------------------

class TestAddClaim(unittest.TestCase):

    def _setup(self, tmp: str) -> tuple[Path, str]:
        root = Path(tmp)
        digest = K.import_source(root, _make_source())
        return root, digest

    def test_stores_claim_with_captured_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            (root / "wiki").mkdir(parents=True, exist_ok=True)
            K.add_claim(root, _make_claim("c1", "src-1", digest))
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            c = store["claims"]["c1"]
            self.assertEqual(c["status"], "captured")
            self.assertEqual(c["source_revision"], digest)

    def test_returns_claim_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            claim_id = K.add_claim(root, _make_claim("c42", "src-1", digest))
            self.assertEqual(claim_id, "c42")

    def test_idempotent_same_claim_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            K.add_claim(root, _make_claim("c1", "src-1", digest))
            K.add_claim(root, _make_claim("c1", "src-1", digest))
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertEqual(len(store["claims"]), 1)

    def test_rejects_unknown_source_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError) as ctx:
                K.add_claim(root, _make_claim("c1", "no-such-src", "aabbcc"))
            self.assertIn("unknown source_id", str(ctx.exception))

    def test_rejects_wrong_source_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            wrong_rev = "0" * 64
            with self.assertRaises(ValueError) as ctx:
                K.add_claim(root, _make_claim("c1", "src-1", wrong_rev))
            self.assertIn("revision mismatch", str(ctx.exception))

    def test_rejects_missing_required_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            claim = _make_claim("c1", "src-1", digest)
            del claim["subject"]
            with self.assertRaises(ValueError) as ctx:
                K.add_claim(root, claim)
            self.assertIn("subject", str(ctx.exception))

    def test_effective_at_optional(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, digest = self._setup(tmp)
            claim = _make_claim("c1", "src-1", digest)
            del claim["effective_at"]
            K.add_claim(root, claim)
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertIsNone(store["claims"]["c1"]["effective_at"])


# ---------------------------------------------------------------------------
# review_claim
# ---------------------------------------------------------------------------

class TestReviewClaim(unittest.TestCase):

    def _setup_with_claim(self, tmp: str) -> tuple[Path, str]:
        root = Path(tmp)
        digest = K.import_source(root, _make_source())
        K.add_claim(root, _make_claim("c1", "src-1", digest))
        return root, digest

    def test_sets_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self._setup_with_claim(tmp)
            K.review_claim(root, "c1", "accepted")
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertEqual(store["claims"]["c1"]["status"], "accepted")

    def test_sets_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self._setup_with_claim(tmp)
            K.review_claim(root, "c1", "rejected")
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertEqual(store["claims"]["c1"]["status"], "rejected")

    def test_rejects_invalid_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self._setup_with_claim(tmp)
            with self.assertRaises(ValueError) as ctx:
                K.review_claim(root, "c1", "approved")
            self.assertIn("invalid status", str(ctx.exception))

    def test_rejects_unknown_claim_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir(parents=True, exist_ok=True)
            (root / "wiki" / "knowledge.json").write_text(
                json.dumps({"sources": {}, "claims": {}}), encoding="utf-8"
            )
            with self.assertRaises(ValueError) as ctx:
                K.review_claim(root, "no-such-claim", "accepted")
            self.assertIn("unknown claim_id", str(ctx.exception))

    def test_captured_disputed_cannot_silently_become_accepted(self):
        """Disputed claims must go through explicit review_claim('accepted')."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self._setup_with_claim(tmp)
            K.review_claim(root, "c1", "disputed")
            # it stays disputed without explicit acceptance
            store = json.loads((root / "wiki" / "knowledge.json").read_text())
            self.assertEqual(store["claims"]["c1"]["status"], "disputed")

    def test_all_valid_statuses_accepted(self):
        valid = {"captured", "extracted", "accepted", "rejected", "disputed", "superseded"}
        for status in valid:
            with tempfile.TemporaryDirectory() as tmp:
                root, _ = self._setup_with_claim(tmp)
                K.review_claim(root, "c1", status)
                store = json.loads((root / "wiki" / "knowledge.json").read_text())
                self.assertEqual(store["claims"]["c1"]["status"], status)


# ---------------------------------------------------------------------------
# retrieve
# ---------------------------------------------------------------------------

def _make_wiki_with_page(root: Path, page_name: str = "topic.md", index: bool = True) -> Path:
    wiki = root / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    page_path = wiki / page_name
    page_path.write_text(f"# {page_name}\nSome content.", encoding="utf-8")
    if index:
        (wiki / "index.md").write_text(f"- [{page_name}]({page_name})\n", encoding="utf-8")
    return page_path


class TestRetrieve(unittest.TestCase):

    def _full_setup(
        self, tmp: str, page: str = "topic.md", num_claims: int = 1
    ) -> tuple[Path, list[str], str]:
        root = Path(tmp)
        _make_wiki_with_page(root, page)
        digest = K.import_source(root, _make_source())
        claim_ids = []
        for i in range(num_claims):
            cid = f"c{i+1}"
            K.add_claim(root, _make_claim(cid, "src-1", digest, page=page))
            K.review_claim(root, cid, "accepted")
            claim_ids.append(cid)
        return root, claim_ids, digest

    def test_returns_accepted_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, claim_ids, _ = self._full_setup(tmp)
            result = K.retrieve(root, "topic.md")
            self.assertEqual(result["page"], "topic.md")
            ids_returned = {c["id"] for c in result["claims"]}
            self.assertEqual(ids_returned, set(claim_ids))

    def test_only_accepted_claims_eligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            digest = K.import_source(root, _make_source())
            K.add_claim(root, _make_claim("c1", "src-1", digest, page="topic.md"))
            K.add_claim(root, _make_claim("c2", "src-1", digest, page="topic.md"))
            K.review_claim(root, "c1", "accepted")
            K.review_claim(root, "c2", "rejected")
            result = K.retrieve(root, "topic.md")
            ids = {c["id"] for c in result["claims"]}
            self.assertIn("c1", ids)
            self.assertNotIn("c2", ids)

    def test_returns_page_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _, _ = self._full_setup(tmp)
            result = K.retrieve(root, "topic.md")
            self.assertIsNotNone(result["text"])
            self.assertIn("topic.md", result["text"])

    def test_gaps_for_null_body_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            digest = K.import_source(root, _make_source(body=None))
            K.add_claim(root, _make_claim("c1", "src-1", digest, page="topic.md"))
            K.review_claim(root, "c1", "accepted")
            result = K.retrieve(root, "topic.md")
            self.assertIn("src-1", result["gaps"])

    def test_no_gaps_for_body_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _, _ = self._full_setup(tmp)
            result = K.retrieve(root, "topic.md")
            self.assertEqual(result["gaps"], [])

    def test_conflicts_for_same_subject_predicate_different_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            d1 = K.import_source(root, {"id": "s1", "body": "first", "url": ""})
            d2 = K.import_source(root, {"id": "s2", "body": "second", "url": ""})
            K.add_claim(root, _make_claim("c1", "s1", d1, page="topic.md", statement="0.5.0"))
            K.add_claim(root, _make_claim("c2", "s2", d2, page="topic.md", statement="0.6.0"))
            K.review_claim(root, "c1", "accepted")
            K.review_claim(root, "c2", "accepted")
            result = K.retrieve(root, "topic.md")
            self.assertEqual(len(result["conflicts"]), 1)
            conflict_ids = {c["id"] for g in result["conflicts"] for c in g}
            self.assertEqual(conflict_ids, {"c1", "c2"})

    def test_no_conflicts_when_same_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            d1 = K.import_source(root, {"id": "s1", "body": "first", "url": ""})
            d2 = K.import_source(root, {"id": "s2", "body": "second", "url": ""})
            K.add_claim(root, _make_claim("c1", "s1", d1, page="topic.md", statement="0.5.0"))
            K.add_claim(root, _make_claim("c2", "s2", d2, page="topic.md", statement="0.5.0"))
            K.review_claim(root, "c1", "accepted")
            K.review_claim(root, "c2", "accepted")
            result = K.retrieve(root, "topic.md")
            self.assertEqual(result["conflicts"], [])

    def test_returns_source_revision_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _, digest = self._full_setup(tmp)
            result = K.retrieve(root, "topic.md")
            self.assertIn("src-1", result["sources"])
            self.assertEqual(result["sources"]["src-1"]["revision"], digest)

    def test_missing_page_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir(parents=True)
            (root / "wiki" / "index.md").write_text("- [other](other.md)\n", encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                K.retrieve(root, "nonexistent.md")
            self.assertIn("not found", str(ctx.exception).lower())

    def test_missing_wiki_dir_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                K.retrieve(root, "topic.md")

    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir(parents=True)
            with self.assertRaises(ValueError) as ctx:
                K.retrieve(root, "../escape.md")
            self.assertIn("escapes", str(ctx.exception).lower())

    def test_unindexed_page_rejected(self):
        """A page file that exists but is not in index.md should be rejected."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = root / "wiki"
            wiki.mkdir(parents=True)
            (wiki / "secret.md").write_text("hidden", encoding="utf-8")
            (wiki / "other.md").write_text("Other", encoding="utf-8")
            (wiki / "index.md").write_text("- [other](other.md)\n", encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                K.retrieve(root, "secret.md")
            self.assertIn("not indexed", str(ctx.exception).lower())

    def test_conflicts_not_suppressed(self):
        """Conflicting accepted claims must surface, never be hidden."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            d1 = K.import_source(root, {"id": "s1", "body": "text1", "url": ""})
            d2 = K.import_source(root, {"id": "s2", "body": "text2", "url": ""})
            K.add_claim(root, _make_claim("c1", "s1", d1, page="topic.md", predicate="price", statement="$100"))
            K.add_claim(root, _make_claim("c2", "s2", d2, page="topic.md", predicate="price", statement="$200"))
            K.review_claim(root, "c1", "accepted")
            K.review_claim(root, "c2", "accepted")
            result = K.retrieve(root, "topic.md")
            self.assertGreater(len(result["conflicts"]), 0, "conflicts must not be suppressed")

    def test_empty_store_returns_empty_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_wiki_with_page(root, "topic.md")
            # knowledge.json not yet created: retrieve should still work
            result = K.retrieve(root, "topic.md")
            self.assertEqual(result["claims"], [])
            self.assertEqual(result["gaps"], [])
            self.assertEqual(result["conflicts"], [])


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

class TestCLI(unittest.TestCase):

    def test_import_source_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "--root", tmp,
                "import-source",
                "--id", "art-1",
                "--url", "https://example.com/art",
                "--author", "J. Doe",
                "--body", "Full article text.",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["id"], "art-1")
            self.assertEqual(len(data["revision"]), 64)

    def test_import_source_null_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "--root", tmp,
                "import-source",
                "--id", "art-missing",
                "--url", "https://example.com/art",
                "--completeness", "missing",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_add_claim_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            # first import source
            imp = _run(
                "--root", tmp,
                "import-source",
                "--id", "s1",
                "--body", "body text",
            )
            self.assertEqual(imp.returncode, 0)
            digest = json.loads(imp.stdout)["revision"]
            # add claim
            result = _run(
                "--root", tmp,
                "add-claim",
                "--id", "c1",
                "--subject", "Factor",
                "--predicate", "version",
                "--statement", "0.5.0",
                "--source-id", "s1",
                "--source-revision", digest,
                "--locator", "§ 1",
                "--page", "topic.md",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["claim_id"], "c1")

    def test_add_claim_wrong_revision_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            _run("--root", tmp, "import-source", "--id", "s1", "--body", "b")
            result = _run(
                "--root", tmp,
                "add-claim",
                "--id", "c1",
                "--subject", "X",
                "--predicate", "y",
                "--statement", "z",
                "--source-id", "s1",
                "--source-revision", "0" * 64,
                "--locator", "§1",
                "--page", "p.md",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("revision mismatch", result.stderr)

    def test_review_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            imp = _run("--root", tmp, "import-source", "--id", "s1", "--body", "b")
            digest = json.loads(imp.stdout)["revision"]
            _run(
                "--root", tmp, "add-claim",
                "--id", "c1", "--subject", "X", "--predicate", "p",
                "--statement", "v", "--source-id", "s1",
                "--source-revision", digest, "--locator", "§1", "--page", "pg.md",
            )
            result = _run("--root", tmp, "review", "--claim-id", "c1", "--status", "accepted")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "accepted")

    def test_review_invalid_status_exits_2(self):
        result = _run("--root", "/tmp", "review", "--claim-id", "c1", "--status", "SUPERACCEPTED")
        self.assertNotEqual(result.returncode, 0)

    def test_retrieve_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = root / "wiki"
            wiki.mkdir()
            (wiki / "page.md").write_text("# Page\nContent.", encoding="utf-8")
            (wiki / "index.md").write_text("- [page](page.md)\n", encoding="utf-8")

            imp = _run("--root", tmp, "import-source", "--id", "s1", "--body", "b")
            digest = json.loads(imp.stdout)["revision"]
            _run(
                "--root", tmp, "add-claim",
                "--id", "c1", "--subject", "X", "--predicate", "p",
                "--statement", "v", "--source-id", "s1",
                "--source-revision", digest, "--locator", "§1", "--page", "page.md",
            )
            _run("--root", tmp, "review", "--claim-id", "c1", "--status", "accepted")

            result = _run("--root", tmp, "retrieve", "--page", "page.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["page"], "page.md")
            self.assertEqual(len(data["claims"]), 1)
            self.assertEqual(data["claims"][0]["id"], "c1")

    def test_retrieve_missing_page_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir()
            (root / "wiki" / "index.md").write_text("- [other](other.md)\n", encoding="utf-8")
            result = _run("--root", tmp, "retrieve", "--page", "missing.md")
            self.assertEqual(result.returncode, 1)

    def test_no_subcommand_exits_2(self):
        result = _run("--root", "/tmp")
        self.assertEqual(result.returncode, 2)


# ---------------------------------------------------------------------------
# Safe path helper
# ---------------------------------------------------------------------------

class TestSafeChild(unittest.TestCase):

    def test_normal_path_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = K._safe_child(root, "wiki/topic.md")
            # _safe_child returns a resolved path; compare against resolved root
            self.assertTrue(result.is_relative_to(root.resolve()))

    def test_traversal_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                K._safe_child(root, "../outside.txt")

    def test_symlink_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            link = root / "link"
            link.symlink_to("/etc")
            with self.assertRaises(ValueError):
                K._safe_child(root, "link/passwd")




class TestKnowledgeHardening(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "company"
        self.root.mkdir()
        _make_wiki_with_page(self.root)
        self.digest = K.import_source(self.root, _make_source())

    def claim(self, **updates):
        claim = _make_claim("c1", "src-1", self.digest)
        claim.update(updates)
        return claim

    def accept(self, **updates):
        claim = self.claim(**updates)
        K.add_claim(self.root, claim)
        K.review_claim(self.root, claim["id"], "accepted")

    def store(self):
        return json.loads((self.root / "wiki/knowledge.json").read_text())

    def write_store(self, store):
        (self.root / "wiki/knowledge.json").write_text(json.dumps(store))

    def test_old_body_preserved_and_stale_claim_reported(self):
        self.accept()
        new = K.import_source(self.root, _make_source(body="new body"))
        result = K.retrieve(self.root, "topic")
        self.assertEqual(result["claims"][0]["source_revision"], self.digest)
        self.assertNotIn("body", result["sources"]["src-1"]["revisions"][self.digest])
        self.assertEqual(self.store()["sources"]["src-1"]["revisions"][self.digest]["body"], "Article body.")
        self.assertEqual(result["stale_revisions"], [{"claim_id": "c1", "source_id": "src-1",
                        "source_revision": self.digest, "latest_revision": new}])
        K.add_claim(self.root, self.claim(id="old-evidence"))
        self.assertEqual(len(self.store()["sources"]["src-1"]["revisions"]), 2)

    def test_exact_utf8_content_hash_and_missing_distinct_from_empty(self):
        text = "é\r\n  "
        digest = K.import_source(self.root, {"id": "utf8", "body": text})
        self.assertEqual(digest, hashlib.sha256(text.encode("utf-8")).hexdigest())
        missing = K.import_source(self.root, {"id": "blank", "body": None})
        empty = K.import_source(self.root, {"id": "blank", "body": ""})
        self.assertNotEqual(missing, empty)
        self.assertEqual(empty, hashlib.sha256(b"").hexdigest())
        self.assertIsNone(self.store()["sources"]["blank"]["revisions"][missing]["content_sha256"])

    def test_idempotence_does_not_reset_review_or_latest_revision(self):
        self.accept()
        K.add_claim(self.root, self.claim())
        new = K.import_source(self.root, _make_source(body="new"))
        K.import_source(self.root, _make_source())
        self.assertEqual(self.store()["claims"]["c1"]["status"], "accepted")
        self.assertEqual(self.store()["sources"]["src-1"]["revision"], new)

    def test_same_claim_id_conflicting_content_rejected_without_write(self):
        self.accept()
        before = (self.root / "wiki/knowledge.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "conflicting"):
            K.add_claim(self.root, self.claim(statement="different"))
        self.assertEqual((self.root / "wiki/knowledge.json").read_bytes(), before)

    def test_claim_status_cannot_bypass_review(self):
        with self.assertRaisesRegex(ValueError, "review explicitly"):
            K.add_claim(self.root, self.claim(status="accepted"))

    def test_source_metadata_cannot_mutate_existing_revision(self):
        source = _make_source()
        source["url"] = "https://different.example/"
        with self.assertRaisesRegex(ValueError, "conflicting metadata"):
            K.import_source(self.root, source)

    def test_missing_source_or_revision_in_store_fail_closed(self):
        self.accept()
        original = self.store()
        for corrupt in ("source", "revision"):
            with self.subTest(corrupt=corrupt):
                store = json.loads(json.dumps(original))
                if corrupt == "source":
                    store["sources"] = {}
                else:
                    store["claims"]["c1"]["source_revision"] = "0" * 64
                self.write_store(store)
                with self.assertRaisesRegex(ValueError, "missing source"):
                    K.retrieve(self.root, "topic.md")

    def test_corrupt_record_types_hashes_and_status_fail_closed(self):
        self.accept()
        original = self.store()
        variants = [[], {"sources": [], "claims": {}}, {"sources": {}, "claims": []}]
        for field, value in (("body", 42), ("content_sha256", "0" * 64), ("completeness", [])):
            store = json.loads(json.dumps(original))
            store["sources"]["src-1"][field] = value
            variants.append(store)
        for field, value in (("status", "approved"), ("statement", 12), ("effective_at", [])):
            store = json.loads(json.dumps(original))
            store["claims"]["c1"][field] = value
            variants.append(store)
        for store in variants:
            with self.subTest(store=store):
                self.write_store(store)
                with self.assertRaises(ValueError):
                    K.retrieve(self.root, "topic.md")

    def test_index_requires_real_links_and_rejects_broken_external_traversal(self):
        index = self.root / "wiki/index.md"
        for text in ("topic.md", "[topic.md](other.md)", "`[topic](topic.md)`",
                     "<!-- [[topic]] -->", "[topic](https://example.com/topic.md)",
                     "[topic](../topic.md)", "[topic](%2e%2e/topic.md)",
                     "[topic](topic.md)\n[broken](broken.md)"):
            with self.subTest(text=text):
                index.write_text(text)
                with self.assertRaises(ValueError):
                    K.retrieve(self.root, "topic.md")
        index.unlink()
        with self.assertRaisesRegex(ValueError, "required"):
            K.retrieve(self.root, "topic.md")

    def test_path_qualified_links_and_unique_legacy_wiki_stem(self):
        wiki = self.root / "wiki"
        (wiki / "people").mkdir()
        (wiki / "people/owner.md").write_text("Owner")
        for link in ("[[owner]]", "[[people/owner|Owner]]", "[Owner](people/owner.md#identity)"):
            (wiki / "index.md").write_text(link)
            result = K.retrieve(self.root, "people/owner.md")
            self.assertEqual(result["page"], "people/owner.md")
        (wiki / "index.md").write_text("[[owner]]")
        self.assertEqual(K.retrieve(self.root, "owner")["page"], "people/owner.md")
        (wiki / "owner.md").write_text("ambiguous")
        with self.assertRaisesRegex(ValueError, "uniquely"):
            K.retrieve(self.root, "people/owner.md")

    def test_normalized_page_claims_do_not_cross_basenames(self):
        wiki = self.root / "wiki"
        (wiki / "other").mkdir()
        (wiki / "other/topic.md").write_text("Other topic")
        (wiki / "index.md").write_text("[[topic.md]]\n[[other/topic.md]]")
        # Use path-qualified Markdown links to avoid intentionally ambiguous wiki stems.
        (wiki / "index.md").write_text("[a](topic.md)\n[b](other/topic.md)")
        self.accept(page="./wiki/topic")
        self.assertEqual(len(K.retrieve(self.root, "topic.md")["claims"]), 1)
        self.assertEqual(K.retrieve(self.root, "other/topic.md")["claims"], [])

    def test_all_storage_and_read_symlinks_rejected_without_touching_target(self):
        outer = Path(self.temp.name) / "outside"
        outer.mkdir()
        sentinel = outer / "sentinel"
        sentinel.write_text("untouched")
        for relative in ("wiki/knowledge.json", "wiki/knowledge.json.new", "wiki/index.md", "wiki/topic.md"):
            with self.subTest(relative=relative):
                path = self.root / relative
                saved = path.read_bytes() if path.exists() else None
                if path.exists():
                    path.unlink()
                path.symlink_to(sentinel)
                try:
                    if relative.endswith(".new"):
                        with self.assertRaises(ValueError):
                            K.import_source(self.root, {"id": "new", "body": "new"})
                    else:
                        with self.assertRaises(ValueError):
                            K.retrieve(self.root, "topic.md")
                    self.assertEqual(sentinel.read_text(), "untouched")
                finally:
                    path.unlink()
                    if saved is not None:
                        path.write_bytes(saved)
        alias = Path(self.temp.name) / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            K.import_source(alias, {"id": "new", "body": "new"})
        company = Path(self.temp.name) / "othercompany"
        company.mkdir()
        (company / "wiki").symlink_to(outer, target_is_directory=True)
        with self.assertRaises(ValueError):
            K.import_source(company, {"id": "new", "body": "new"})
        self.assertFalse((outer / "knowledge.json").exists())

    def test_traversal_and_symlink_claim_paths_rejected(self):
        (self.root / "wiki/linked").symlink_to(Path(self.temp.name), target_is_directory=True)
        for page in ("../outside.md", "x/../topic.md", "/tmp/topic.md", "%2e%2e/topic.md", "linked/page.md"):
            with self.subTest(page=page), self.assertRaises(ValueError):
                K.add_claim(self.root, self.claim(page=page))

    def test_partial_body_is_visible_gap(self):
        source = _make_source()
        source.update(id="partial", completeness="partial")
        digest = K.import_source(self.root, source)
        self.accept(source_id="partial", source_revision=digest)
        self.assertEqual(K.retrieve(self.root, "topic.md")["gaps"], ["partial"])

    def test_index_checker_collects_all_errors_and_supports_missing_legacy_index(self):
        index = self.root / "wiki/index.md"
        index.write_text("[[ghost]]\n[absent](absent.md)\n[escape](../outside.md)")
        problems = K.wiki_index_problems(self.root)
        self.assertEqual(len(problems), 3)
        self.assertIn("missing wiki page ghost", problems[0])
        index.unlink()
        self.assertEqual(K.wiki_index_problems(self.root), [])

    def test_duplicate_json_record_keys_rejected(self):
        (self.root / "wiki/knowledge.json").write_text('{"sources": {}, "claims": {}, "claims": {}}')
        with self.assertRaisesRegex(ValueError, "duplicate"):
            K.retrieve(self.root, "topic.md")

    def test_malformed_json_cli_fails_without_traceback(self):
        (self.root / "wiki/knowledge.json").write_text("{")
        result = _run("--root", str(self.root), "retrieve", "--page", "topic.md")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
