import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONBOARD = ROOT / "scripts" / "onboard.py"
NEW = ROOT / "scripts" / "new-company.sh"


class OnboardTest(unittest.TestCase):
    def test_json_groups_the_three_categories_and_skips_composio(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        categories = {row["category"] for row in rows}
        self.assertEqual(categories, {"skills", "plugins", "other"})
        ids = {row["id"] for row in rows}
        self.assertIn("openspec", ids)
        self.assertIn("refactoring-ui", ids)
        self.assertIn("tinyfish", ids)
        self.assertIn("clawhub", ids)
        self.assertNotIn("composio", ids)
        offered_skills = [
            row for row in rows if row["category"] == "skills" and row["disposition"] == "add"
        ]
        self.assertGreaterEqual(len(offered_skills), 20)
        skill_file = ROOT / "catalog" / "cards" / "openspec" / "SKILL.md"
        self.assertFalse((ROOT / "skills" / "catalog").exists())
        self.assertTrue(skill_file.is_file())
        self.assertNotIn("composio", skill_file.read_text(encoding="utf-8").lower())

    def test_enable_writes_the_company_and_refuses_shelf(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            enabled = subprocess.run(
                [
                    sys.executable,
                    str(ONBOARD),
                    "--company",
                    str(dest),
                    "--enable",
                    "openspec,ffmpeg-skill",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(enabled.returncode, 0, enabled.stderr)
            text = (dest / "connectors" / "enabled.yaml").read_text(encoding="utf-8")
            self.assertIn("id: openspec", text)
            self.assertIn("category: skills", text)
            copied = (dest / "skills" / "openspec" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Fission-AI/OpenSpec", copied)
            checked = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check_company.py"), str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertNotIn("missing card", checked.stdout)
            self.assertNotIn("connector openspec", checked.stdout)
            refused = subprocess.run(
                [sys.executable, str(ONBOARD), "--enable", "goose"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(refused.returncode, 1)
            self.assertIn("shelf", refused.stderr)

    def test_plugin_category_copies_only_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            enabled = subprocess.run(
                [
                    sys.executable,
                    str(ONBOARD),
                    "--company",
                    str(dest),
                    "--enable-category",
                    "plugins",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(enabled.returncode, 0, enabled.stderr)
            text = (dest / "connectors" / "enabled.yaml").read_text(encoding="utf-8")
            self.assertIn("id: refactoring-ui", text)
            self.assertIn("id: pixelrag", text)
            self.assertNotIn("id: openspec", text)
            self.assertTrue((dest / "skills" / "pixelrag" / "SKILL.md").is_file())

    def test_harvest_writes_soul_before_tools(self):
        harvest = (
            "## Owner\n\nAda, decides in writing.\n"
            "## Soul\n\nShort sentences. No invented prices.\n"
            "## Company\n\nA studio that ships one product.\n"
            "## Customer\n\nPeople who already tried a template.\n"
            "## Offer\n\nFILL: price not in the repo.\n"
            "## Positioning\n\nChosen for the voice.\n"
            "## Voice\n\nPlain speech.\n"
            "## Proof\n\nNo approved claims yet.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harvest_path = root / "factor-harvest.md"
            harvest_path.write_text(harvest, encoding="utf-8")
            dest = root / "acme"
            made = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            applied = subprocess.run(
                [
                    sys.executable,
                    str(ONBOARD),
                    "--company",
                    str(dest),
                    "--apply-harvest",
                    str(harvest_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            soul = (dest / "SOUL.md").read_text(encoding="utf-8")
            self.assertIn("Ada, decides in writing.", soul)
            self.assertIn("Short sentences.", soul)
            self.assertIn("FILL: price not in the repo.", (dest / "context" / "offer.md").read_text(encoding="utf-8"))
            steps = subprocess.run(
                [sys.executable, str(ONBOARD), "--steps"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(steps.returncode, 0, steps.stderr)
            self.assertIn("1. Harvest", steps.stdout)
            self.assertIn("SOUL.md", steps.stdout)
            self.assertLess(steps.stdout.find("1. Harvest"), steps.stdout.find("3. Choose"))

    def test_pipe_prints_and_exits(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD)],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SKILLS", result.stdout)

    def test_text_category_is_noninteractive(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--text", "--category", "plugins"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PLUGINS", result.stdout)
        self.assertIn("refactoring-ui", result.stdout)
        self.assertNotIn("SKILLS", result.stdout)


if __name__ == "__main__":
    unittest.main()
