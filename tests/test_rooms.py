import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "scripts" / "new-company.sh"
ROOMS = ROOT / "scripts" / "rooms.py"


class RoomTest(unittest.TestCase):
    def test_a_new_company_holds_the_rooms(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            checked = subprocess.run(
                [sys.executable, str(ROOMS), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout)
            brief = (dest / "desks" / "content" / "brief.md").read_text(encoding="utf-8")
            self.assertIn("Page:", brief)
            self.assertIn("does not publish", brief)
            report = (dest / "desks" / "numbers" / "report.md").read_text(encoding="utf-8")
            self.assertIn("## Figures", report)
            self.assertIn("## Suggestion", report)
            self.assertIn("Stay quiet", report)

    def test_numbers_stay_quiet_when_no_line_was_crossed(self):
        spec = __import__("importlib.util").util.spec_from_file_location("rooms", ROOMS)
        module = __import__("importlib.util").util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertIsNone(module.numbers_message(False))
        self.assertEqual(module.numbers_message(True), "report")


if __name__ == "__main__":
    unittest.main()
