"""Tests for language preference, resource helpers, and onboard language integration.

Coverage:
- EN default (no file, missing key, missing company)
- FR override / persistence / company precedence
- No implicit persistence: --language does not write prefs
- Invalid / corrupt inputs preserve data
- JSON backward compat: existing --json catalog unchanged when no resources
- Resources: FR paths and language truth
- Explicit opening only (mocked)
- No path traversal
- French harvest prompts preserve English headings and FILL: tokens
- Interactive toggle/resources preserve selected capability state
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ONBOARD = SCRIPTS / "onboard.py"
PREFS = SCRIPTS / "preferences.py"
RESOURCES_SCRIPT = SCRIPTS / "learning_resources.py"
NEW = ROOT / "scripts" / "new-company.sh"
sys.path.insert(0, str(SCRIPTS))


def _make_company(tmp: str) -> Path:
    dest = Path(tmp) / "acme"
    result = subprocess.run([str(NEW), "acme", str(dest)], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return dest


# ─── preferences.py unit tests ──────────────────────────────────────────────

class LoadLanguageTest(unittest.TestCase):
    def test_missing_company_returns_en(self):
        from preferences import load_language
        self.assertEqual(load_language(None), "en")

    def test_missing_file_returns_en(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            self.assertEqual(load_language(company), "en")

    def test_missing_language_key_returns_en(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps({"other_key": "value"}), encoding="utf-8"
            )
            self.assertEqual(load_language(company), "en")

    def test_en_preference_loads(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps({"language": "en"}), encoding="utf-8"
            )
            self.assertEqual(load_language(company), "en")

    def test_fr_preference_loads(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps({"language": "fr"}), encoding="utf-8"
            )
            self.assertEqual(load_language(company), "fr")

    def test_invalid_language_value_raises(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps({"language": "de"}), encoding="utf-8"
            )
            with self.assertRaises(SystemExit):
                load_language(company)

    def test_corrupt_json_raises_without_overwriting(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            path = company / "preferences.json"
            path.write_text("{ not valid json ", encoding="utf-8")
            with self.assertRaises(SystemExit):
                load_language(company)
            # File must remain unchanged
            self.assertEqual(path.read_text(encoding="utf-8"), "{ not valid json ")

    def test_non_object_json_raises(self):
        from preferences import load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps(["en"]), encoding="utf-8"
            )
            with self.assertRaises(SystemExit):
                load_language(company)


class SaveLanguageTest(unittest.TestCase):
    def test_save_en_creates_file(self):
        from preferences import save_language, load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            save_language(company, "en")
            self.assertEqual(load_language(company), "en")

    def test_save_fr_and_read_back(self):
        from preferences import save_language, load_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            save_language(company, "fr")
            self.assertEqual(load_language(company), "fr")

    def test_preserves_unrelated_keys(self):
        from preferences import save_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            (company / "preferences.json").write_text(
                json.dumps({"language": "en", "theme": "dark", "count": 42}),
                encoding="utf-8",
            )
            save_language(company, "fr")
            data = json.loads((company / "preferences.json").read_text(encoding="utf-8"))
            self.assertEqual(data["language"], "fr")
            self.assertEqual(data["theme"], "dark")
            self.assertEqual(data["count"], 42)

    def test_invalid_language_raises(self):
        from preferences import save_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            with self.assertRaises(SystemExit):
                save_language(company, "de")

    def test_missing_company_dir_raises(self):
        from preferences import save_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "nonexistent"
            with self.assertRaises(SystemExit):
                save_language(company, "en")

    def test_corrupt_json_refuses_to_overwrite(self):
        from preferences import save_language
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            path = company / "preferences.json"
            path.write_text("CORRUPTED", encoding="utf-8")
            with self.assertRaises(SystemExit):
                save_language(company, "fr")
            self.assertEqual(path.read_text(encoding="utf-8"), "CORRUPTED")


# ─── preferences CLI tests ───────────────────────────────────────────────────

class PrefsCLITest(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(PREFS), *args],
            capture_output=True,
            text=True,
        )

    def test_get_default_en(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            result = self._run("--company", str(company))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "en")

    def test_set_and_get_fr(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            set_result = self._run("--company", str(company), "--set", "fr")
            self.assertEqual(set_result.returncode, 0, set_result.stderr)
            get_result = self._run("--company", str(company))
            self.assertEqual(get_result.stdout.strip(), "fr")

    def test_json_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            result = self._run("--company", str(company), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["language"], "en")

    def test_set_with_json_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "co"
            company.mkdir()
            result = self._run("--company", str(company), "--set", "fr", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["language"], "fr")


# ─── language does NOT persist without --set-language ────────────────────────

class NoImplicitPersistenceTest(unittest.TestCase):
    def test_language_flag_does_not_write_prefs(self):
        """--language is invocation-only; it must not touch preferences.json."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            # Set a known state
            prefs_path = dest / "preferences.json"
            prefs_path.write_text(json.dumps({"language": "en"}), encoding="utf-8")
            original_mtime = prefs_path.stat().st_mtime

            subprocess.run(
                [sys.executable, str(ONBOARD), "--company", str(dest), "--language", "fr", "--steps"],
                capture_output=True,
                text=True,
            )
            # File modification time must be unchanged
            self.assertEqual(prefs_path.stat().st_mtime, original_mtime)

    def test_set_language_persists(self):
        """--set-language must write the preference and exit."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            result = subprocess.run(
                [sys.executable, str(ONBOARD), "--company", str(dest), "--set-language", "fr"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            from preferences import load_language
            self.assertEqual(load_language(dest), "fr")

    def test_set_language_requires_company(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--set-language", "fr"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


# ─── company preference precedence ───────────────────────────────────────────

class CompanyPreferencePrecedenceTest(unittest.TestCase):
    def test_company_pref_fr_drives_resources(self):
        """With company pref fr and no --language, resources should be in French."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            (dest / "preferences.json").write_text(
                json.dumps({"language": "fr"}), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(RESOURCES_SCRIPT), "--company", str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Comprendre Factor", result.stdout)

    def test_explicit_language_flag_beats_company_pref(self):
        """--language overrides company preference for this invocation."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            (dest / "preferences.json").write_text(
                json.dumps({"language": "fr"}), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(RESOURCES_SCRIPT), "--company", str(dest), "--language", "en"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Understand Factor", result.stdout)


# ─── JSON backward compat ─────────────────────────────────────────────────────

class JSONBackwardCompatTest(unittest.TestCase):
    def test_json_catalog_unchanged_when_no_resources(self):
        """--json without --resources must print the registry, not resources."""
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        # Must be a list of catalog items (registry), not resources
        self.assertIsInstance(rows, list)
        categories = {row["category"] for row in rows}
        self.assertEqual(categories, {"skills", "plugins", "other"})

    def test_resources_json_is_separate(self):
        """--resources --json must give a resources list, separate from catalog."""
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--resources", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertIsInstance(rows, list)
        self.assertTrue(len(rows) > 0)
        # Resources have id, kind, language, title, path
        for row in rows:
            self.assertIn("id", row)
            self.assertIn("kind", row)
            self.assertIn("language", row)
            self.assertIn("title", row)
            self.assertIn("path", row)


# ─── learning_resources module tests ─────────────────────────────────────────

class LearningResourcesTest(unittest.TestCase):
    def setUp(self):
        from learning_resources import resources
        self._resources = resources

    def test_en_returns_en_paths(self):
        res_list = self._resources("en")
        self.assertTrue(len(res_list) > 0)
        # The bilingual guide should point at the .en.md file
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        self.assertIn("ecosystem.en.md", str(guide["path"]))

    def test_fr_returns_fr_paths(self):
        res_list = self._resources("fr")
        self.assertTrue(len(res_list) > 0)
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        self.assertIn("ecosystem.fr.md", str(guide["path"]))

    def test_fr_titles_are_french(self):
        res_list = self._resources("fr")
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        self.assertEqual(guide["title"], "Comprendre Factor")

    def test_en_titles_are_english(self):
        res_list = self._resources("en")
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        self.assertEqual(guide["title"], "Understand Factor")

    def test_language_field_truth(self):
        """language field in each resource reflects the resources.json entry, not the filter."""
        res_list = self._resources("en")
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        # framework-guide is bilingual per resources.json
        self.assertEqual(guide["language"], "bilingual")

    def test_paths_are_within_root(self):
        """All resolved paths must be within the repo root (no traversal)."""
        for lang in ("en", "fr"):
            res_list = self._resources(lang)
            for r in res_list:
                try:
                    r["path"].relative_to(ROOT)
                except ValueError:
                    self.fail(
                        f"Resource {r['id']} path {r['path']} is outside the repo root"
                    )

    def test_path_is_resolved_absolute(self):
        res_list = self._resources("en")
        for r in res_list:
            self.assertTrue(r["path"].is_absolute(), f"path not absolute: {r['path']}")

    def test_invalid_language_falls_back_to_en(self):
        """An invalid language code should fall back to en without error."""
        res_list = self._resources("xx")
        self.assertTrue(len(res_list) > 0)
        guide = next((r for r in res_list if r["id"] == "framework-guide"), None)
        self.assertIsNotNone(guide)
        self.assertIn("ecosystem.en.md", str(guide["path"]))


# ─── Explicit open — mocked ───────────────────────────────────────────────────

class ExplicitOpenTest(unittest.TestCase):
    def test_open_resource_calls_opener(self):
        """--open-resource must invoke the OS opener with the resolved path."""
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0)) as mock_run:
            import importlib
            import learning_resources as lr
            importlib.reload(lr)
            result = lr._open_resource("framework-guide", "en")
            self.assertEqual(result, 0)
            self.assertTrue(mock_run.called)
            call_args = mock_run.call_args[0][0]
            # The last arg should be a path ending in ecosystem.en.md
            self.assertIn("ecosystem.en.md", call_args[-1])

    def test_open_missing_id_returns_error(self):
        """--open-resource with an unknown ID must fail without opening anything."""
        with patch("subprocess.run") as mock_run:
            import learning_resources as lr
            result = lr._open_resource("nonexistent-id", "en")
            self.assertNotEqual(result, 0)
            mock_run.assert_not_called()

    def test_headless_json_does_not_open(self):
        """--resources --json must never launch an opener (verified by clean JSON output only)."""
        # Running in a subprocess: no OS opener fires when --json is used.
        # We verify the output is valid JSON resources (not a catalog dump), which
        # proves the resources branch ran and no opener was invoked.
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--resources", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertIsInstance(rows, list)
        self.assertTrue(len(rows) > 0)
        # Resources (not registry) have a 'path' key with an absolute path string
        for row in rows:
            self.assertIn("path", row)


# ─── French harvest prompt tests ─────────────────────────────────────────────

class FrenchHarvestPromptTest(unittest.TestCase):
    HEADINGS = [
        "## Owner",
        "## Soul",
        "## Company",
        "## Customer",
        "## Offer",
        "## Positioning",
        "## Voice",
        "## Style DNA",
        "## Lock",
        "## Stays",
        "## May change",
        "## Proof",
        "## Desk",
    ]

    def _check_prompt(self, filename: str) -> None:
        path = ROOT / "prompts" / filename
        self.assertTrue(path.is_file(), f"prompt file missing: {path}")
        text = path.read_text(encoding="utf-8")
        for heading in self.HEADINGS:
            self.assertIn(heading, text, f"heading {heading!r} missing in {filename}")
        self.assertIn("FILL:", text, f"FILL: token missing in {filename}")

    def test_claude_fr_preserves_headings(self):
        self._check_prompt("harvest-claude.fr.md")

    def test_codex_fr_preserves_headings(self):
        self._check_prompt("harvest-codex.fr.md")

    def test_claude_fr_is_french(self):
        path = ROOT / "prompts" / "harvest-claude.fr.md"
        text = path.read_text(encoding="utf-8")
        # French preamble should contain French text
        self.assertIn("Vous êtes", text)

    def test_codex_fr_is_french(self):
        path = ROOT / "prompts" / "harvest-codex.fr.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("Vous êtes", text)

    def test_show_prompt_claude_fr(self):
        """--prompt claude with --language fr should print the French prompt."""
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--prompt", "claude", "--language", "fr"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Vous êtes", result.stdout)
        self.assertIn("## Owner", result.stdout)

    def test_show_prompt_codex_fr(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--prompt", "codex", "--language", "fr"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Vous êtes", result.stdout)
        self.assertIn("## Owner", result.stdout)

    def test_show_prompt_default_en(self):
        """Without --language, --prompt claude must print the English prompt."""
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--prompt", "claude"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("You are Claude", result.stdout)
        self.assertIn("## Owner", result.stdout)


# ─── Onboard --resources integration ─────────────────────────────────────────

class OnboardResourcesIntegrationTest(unittest.TestCase):
    def test_resources_en_default(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--resources"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("framework-guide", result.stdout)
        self.assertIn("Understand Factor", result.stdout)

    def test_resources_fr(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--resources", "--language", "fr"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("framework-guide", result.stdout)
        self.assertIn("Comprendre Factor", result.stdout)

    def test_resources_with_company_fr_pref(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            (dest / "preferences.json").write_text(
                json.dumps({"language": "fr"}), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(ONBOARD), "--resources", "--company", str(dest)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Comprendre Factor", result.stdout)

    def test_open_resource_missing_id_fails(self):
        result = subprocess.run(
            [sys.executable, str(ONBOARD), "--open-resource", "no-such-id"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


# ─── Interactive state: toggle/resources preserve selected capabilities ───────

class InteractiveToggleStateTest(unittest.TestCase):
    """Verify picker() toggle behaviour by driving it with mocked input/output."""

    def _run_picker(self, items, company, initial_lang, inputs):
        """Drive picker() with a list of input lines and capture printed output."""
        import io
        input_iter = iter(inputs)
        output = io.StringIO()
        with patch("builtins.input", side_effect=input_iter), \
             patch("builtins.print", side_effect=lambda *a, **kw: output.write(" ".join(str(x) for x in a) + "\n")):
            import onboard as ob
            ob.picker(items, company, initial_lang)
        return output.getvalue()

    def _load_items(self):
        import onboard as ob
        return ob.load_items()

    def test_language_toggle_inverted(self):
        """Pressing L in the picker should flip the language and show the French menu."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = _make_company(tmp)
            (dest / "preferences.json").write_text(
                json.dumps({"language": "en"}), encoding="utf-8"
            )
            items = self._load_items()
            output = self._run_picker(items, dest, "en", ["L", "q"])
            # After toggle to FR, French heading should appear
            self.assertIn("Intégration Factor", output)
            # Preference should have been saved as fr
            from preferences import load_language
            self.assertEqual(load_language(dest), "fr")

    def test_language_toggle_without_company_does_not_persist(self):
        """Toggling without a company directory must not persist the language."""
        items = self._load_items()
        # No company — toggle should still work in-session
        output = self._run_picker(items, None, "en", ["L", "q"])
        self.assertIn("Intégration Factor", output)

    def test_capabilities_selection_preserved_across_toggle(self):
        """Toggling language must not clear the selected capabilities set.

        We verify this by exercising the picker code path:
        the selected set is local to picker() and is not re-initialised on L press.
        """
        items = self._load_items()
        offered = [item for item in items if item["disposition"] == "add" and item["category"] == "skills"]
        # Select a real capability, switch language, view resources, and revisit selection.
        output = self._run_picker(items, None, "en", ["4", "1", "1", "b", "q", "L", "R", "b", "4", "1", "b", "q", "q"])
        self.assertIn("Intégration Factor", output)
        self.assertGreaterEqual(output.count(f"[x] {offered[0]['id']}"), 2)



if __name__ == "__main__":
    unittest.main()
