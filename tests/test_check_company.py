import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_company.py"
NEW = ROOT / "scripts" / "new-company.sh"


class CheckCompanyTest(unittest.TestCase):
    def test_template_is_still_blank(self):
        result = subprocess.run(
            [sys.executable, str(CHECK), str(ROOT / "company")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unfilled context/company.md", result.stdout)
        self.assertIn("unnamed AGENTS.md", result.stdout)

    def test_new_company_replaces_the_slug_and_stays_unfilled(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run(
                [str(NEW), "acme", str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(made.returncode, 0, made.stderr)
            agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# acme", agents)
            self.assertNotIn("__COMPANY__", agents)
            checked = subprocess.run(
                [sys.executable, str(CHECK), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(checked.returncode, 1)
            self.assertNotIn("unnamed", checked.stdout)
            self.assertIn("unfilled context/offer.md", checked.stdout)

    def test_rejects_unknown_and_shelf_connectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            enabled = dest / "connectors" / "enabled.yaml"
            enabled.write_text(
                "version: 1\nconnectors:\n  - id: clawhub\n    category: skills\n",
                encoding="utf-8",
            )
            checked = subprocess.run(
                [sys.executable, str(CHECK), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertIn("connector clawhub is shelf", checked.stdout)
            enabled.write_text(
                "version: 1\nconnectors:\n  - id: not-a-real-tool\n",
                encoding="utf-8",
            )
            checked = subprocess.run(
                [sys.executable, str(CHECK), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertIn("unknown connector not-a-real-tool", checked.stdout)

    def test_enabled_id_needs_its_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            enabled = dest / "connectors" / "enabled.yaml"
            enabled.write_text(
                "version: 1\nconnectors:\n  - id: openspec\n    category: skills\n",
                encoding="utf-8",
            )
            checked = subprocess.run(
                [sys.executable, str(CHECK), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertIn("missing card skills/openspec/SKILL.md", checked.stdout)

    def test_rejects_a_bad_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            made = subprocess.run(
                [str(NEW), "Acme Co", str(Path(tmp) / "nope")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(made.returncode, 2)


if __name__ == "__main__":
    unittest.main()
