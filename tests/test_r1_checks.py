import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_company import problems, wiki_problems


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class R1ChecksTest(unittest.TestCase):
    def test_oversized_profile_soul_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "profile-soul.md", "\n".join(f"line {number}" for number in range(81)) + "\n")
            self.assertIn("profile soul exceeds 80 lines", problems(root))

    def test_short_soul_does_not_add_that_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "profile-soul.md", "# Soul\n\n" + ("\n" * 100) + "Short.\n")
            self.assertNotIn("profile soul exceeds 80 lines", problems(root))

    def test_oversized_instinct_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "instinct.md", "\n".join(f"row {number}" for number in range(50)) + "\n")
            self.assertIn("instinct exceeds 40 lines", problems(root))

    def test_wikilink_with_no_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "wiki" / "index.md", "Open [[ghost]] when the work needs it.\n")
            self.assertIn("missing wiki page ghost", problems(root))

    def test_wikilink_whose_file_exists_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "wiki" / "index.md", "The offer is [[offer]]. Skip [[entities/offer]].\n")
            write(root / "wiki" / "entities" / "offer.md", "# Offer\n")
            found = problems(root)
            self.assertNotIn("missing wiki page offer", found)
            self.assertNotIn("missing wiki page entities/offer", found)

    def test_path_qualified_wiki_and_markdown_links_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "wiki/index.md", "[[entities/missing]] [Broken](pages/ghost.md)\n")
            found = wiki_problems(root)
            self.assertEqual(len(found), 2)
            self.assertTrue(any("entities/missing" in error for error in found))
            self.assertTrue(any("pages/ghost.md" in error for error in found))

    def test_matching_stem_outside_wiki_does_not_satisfy_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "wiki/index.md", "[[offer]]\n")
            write(root / "context/offer.md", "# Offer\n")
            self.assertTrue(wiki_problems(root))

    def test_duplicate_bare_stems_fail_until_path_is_qualified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "wiki/index.md", "[[offer]]\n")
            write(root / "wiki/a/offer.md", "First\n")
            write(root / "wiki/b/offer.md", "Second\n")
            self.assertTrue(wiki_problems(root))
            write(root / "wiki/index.md", "[[a/offer]] [Second](b/offer.md)\n")
            self.assertEqual(wiki_problems(root), [])

    def test_traversal_and_symlink_links_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "context/secret.md", "Company context\n")
            write(root / "wiki/index.md", "[Secret](../context/secret.md)\n")
            self.assertTrue(wiki_problems(root))
            (root / "wiki/alias.md").symlink_to(root / "context/secret.md")
            write(root / "wiki/index.md", "[Alias](alias.md)\n")
            self.assertTrue(wiki_problems(root))
            (root / "wiki/index.md").unlink()
            (root / "wiki/index.md").symlink_to(root / "context/secret.md")
            self.assertTrue(wiki_problems(root))

    def test_sourced_price_is_not_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "context" / "offer.md", "The price is $99.\n")
            write(root / "output" / "letter.md", "We charge $99.\n")
            self.assertNotIn("unsourced amount $99 in output/letter.md", problems(root))

    def test_fill_in_a_draft_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "acme"
            write(root / "output" / "README.md", "FILL: this note is not a draft.\n")
            write(root / "output" / "draft.md", "The price is FILL: not in the repo.\n")
            found = problems(root)
            self.assertIn("FILL treated as fact in output/draft.md", found)
            self.assertNotIn("FILL treated as fact in output/README.md", found)


if __name__ == "__main__":
    unittest.main()
