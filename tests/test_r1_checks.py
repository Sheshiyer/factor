import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_company import problems


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
