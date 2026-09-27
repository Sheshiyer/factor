import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "scripts" / "new-company.sh"
ROOMS = ROOT / "scripts" / "rooms.py"


def _load_rooms():
    spec = importlib.util.spec_from_file_location("rooms", ROOMS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class RoomTest(unittest.TestCase):
    def test_a_new_company_holds_the_rooms(self):
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
        mod = _load_rooms()
        self.assertIsNone(mod.numbers_message(False))
        self.assertEqual(mod.numbers_message(True), "report")

    def test_gates_require_approval_required_not_confidence(self):
        """gates.md must declare 'Approval required', not a bare confidence threshold."""
        mod = _load_rooms()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "company"
            desks = root / "desks"
            desks.mkdir(parents=True)
            # A gates.md with a confidence threshold but no 'Approval required'
            gates = desks / "gates.md"
            gates.write_text(
                "# Gates\n\n- Send: wait\n- Spend: wait\n- Publish: wait\n\n"
                "Confidence 0.85 clears the card.\n",
                encoding="utf-8",
            )
            problems = mod.room_problems(root)
            self.assertIn("gates missing Approval required", problems)

    def test_gates_with_approval_required_passes(self):
        """A gates.md with 'Approval required' and all three waits passes."""
        mod = _load_rooms()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "company"
            desks = root / "desks"
            desks.mkdir(parents=True)
            gates = desks / "gates.md"
            gates.write_text(
                "# Gates\n\n- Send: wait\n- Spend: wait\n- Publish: wait\n\n"
                "Approval required. Confidence alone cannot authorise a gated action.\n",
                encoding="utf-8",
            )
            problems = mod.room_problems(root)
            self.assertNotIn("gates missing Approval required", problems)
            self.assertNotIn("gates missing Send: wait", problems)

    def test_new_company_gates_carry_approval_required(self):
        """A freshly created company must have 'Approval required' in gates.md."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "beta"
            made = subprocess.run([str(NEW), "beta", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            gates = (dest / "desks" / "gates.md").read_text(encoding="utf-8")
            self.assertIn("Approval required", gates)
            self.assertNotIn("confidence of 0.85 or an approval comment", gates)


if __name__ == "__main__":
    unittest.main()
