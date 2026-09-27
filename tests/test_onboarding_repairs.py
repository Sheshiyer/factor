"""Exercise actual Python onboarding paths and failure boundaries."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import onboard as ob
import preferences as prefs
import learning_resources as lr


class OnboardingRepairTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.preferences = self.root / "preferences.json"

    def test_combined_flags_save_requested_language_and_display_override(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = ob.main(["onboard", "--company", str(self.root), "--language", "en",
                              "--set-language", "fr", "--steps"])
        self.assertEqual(result, 0)
        self.assertEqual(prefs.load_language(self.root), "fr")
        self.assertIn("Factor onboarding", output.getvalue())
        self.assertNotIn("Intégration Factor", output.getvalue())

    def test_invalid_existing_language_is_preserved_on_save(self):
        for bad in ("es", "", None, [], {}):
            original = json.dumps({"language": bad, "other": "keep"}).encode()
            self.preferences.write_bytes(original)
            with self.subTest(language=bad), self.assertRaises(SystemExit):
                prefs.save_language(self.root, "fr")
            self.assertEqual(self.preferences.read_bytes(), original)

    def test_preferences_reject_all_symlinks_without_changing_them(self):
        target = self.root / "target.json"
        target.write_text('{"language":"en"}')
        outside = self.root.parent / (self.root.name + "-missing")
        for linked in (target, self.root / "dangling", outside):
            with self.subTest(target=linked):
                self.preferences.symlink_to(linked)
                for operation in (lambda: prefs.load_language(self.root),
                                  lambda: prefs.save_language(self.root, "fr")):
                    with self.assertRaisesRegex(SystemExit, "symlink"):
                        operation()
                self.assertTrue(self.preferences.is_symlink())
                self.preferences.unlink()
                self.assertEqual(target.read_text(), '{"language":"en"}')

    def test_preference_io_failures_have_useful_errors_and_preserve_bytes(self):
        self.preferences.write_text('{"language":"en"}')
        before = self.preferences.read_bytes()
        with patch.object(Path, "read_text", side_effect=PermissionError("denied")):
            with self.assertRaisesRegex(SystemExit, "cannot read preferences"):
                prefs.load_language(self.root)
        with patch.object(prefs.os, "replace", side_effect=OSError("disk error")):
            with self.assertRaisesRegex(SystemExit, "cannot save preferences"):
                prefs.save_language(self.root, "fr")
        self.assertEqual(self.preferences.read_bytes(), before)
        self.assertEqual(list(self.root.glob(".prefs-*")), [])

    def test_french_text_and_pipe_translate_owned_catalog_labels(self):
        for flags in (["--text"], []):
            out = io.StringIO()
            with contextlib.redirect_stdout(out), patch.object(sys.stdin, "isatty", return_value=False):
                self.assertEqual(ob.main(["onboard", "--language", "fr", *flags]), 0)
            text = out.getvalue()
            for label in ("COMPÉTENCES", "AUTRES CAPACITÉS", "proposés", "déjà dans Hermes", "Contenu source"):
                self.assertIn(label, text)
            self.assertNotIn("already in Hermes", text)
            self.assertNotIn("Factor onboarding", text)
            self.assertIn(ob.load_items()[0]["summary"], text)

    def test_french_nested_choices_details_and_fixed_lists(self):
        items = [dict(id="one", category="skills", disposition="add", name="Original Name",
                      repo="", kind="skill", risk="local", approval="required",
                      summary="Original English source description", bookmark="https://example.test")]
        items.extend([{**items[0], "id": "built", "disposition": "builtin"},
                      {**items[0], "id": "shelf", "disposition": "shelf"}])
        inputs = iter(["1", "1", "d 1", "d 99", "invalid", "b", "4", "", "5", "", "invalid", "q"])
        prompts, selected, out = [], set(), io.StringIO()
        def respond(prompt):
            prompts.append(prompt)
            return next(inputs)
        with patch("builtins.input", side_effect=respond), contextlib.redirect_stdout(out):
            ob.choose_capabilities(items, items[:1], selected, None, "fr")
        text = out.getvalue()
        for expected in ("Étape 3", "sélectionnés", "Compétences", "Déjà dans Hermes", "Non proposés",
                         "numéro pour sélectionner", "risque", "approbation", "favori", "aucune URL",
                         "aucune commande", "Aucune ligne correspondante", "Pas un choix", "Utilisez"):
            self.assertIn(expected, text)
        self.assertIn("entrée pour revenir ", prompts)
        self.assertIn("Original English source description", text)
        self.assertIn("Original Name", text)
        self.assertEqual(selected, {"one"})
        for english in ("Step 3", "number toggles", "Already in Hermes", "Not offered", "no repository URL"):
            self.assertNotIn(english, text)

    def manifest(self, entries=None):
        path = self.root / "resources.json"
        entry = {"id": "guide", "kind": "guide", "language": "bilingual",
                 "title": {"en": "Guide", "fr": "Guide français"},
                 "paths": {"en": "guide.md"}}
        path.write_text(json.dumps({"resources": [entry] if entries is None else entries}))
        (self.root / "guide.md").write_text("Original source")
        return path, entry

    def test_missing_directories_traversal_and_outside_symlinks_never_open(self):
        manifest, entry = self.manifest()
        (self.root / "directory").mkdir()
        (self.root / "outside").symlink_to(self.root.parent, target_is_directory=True)
        for relative in ("absent.md", "directory", "../outside.md", "outside", str(self.root / "guide.md")):
            manifest.write_text(json.dumps({"resources": [{**entry, "paths": {"en": relative}}]}))
            with patch.object(lr, "ROOT", self.root), patch.object(lr, "RESOURCES_FILE", manifest), \
                 patch.object(lr.subprocess, "run") as run, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(lr.resources(), [])
                self.assertEqual(lr._open_resource("guide", "en"), 1)
                run.assert_not_called()

    def test_inroot_resource_symlink_resolves_to_regular_file(self):
        manifest, entry = self.manifest()
        (self.root / "alias.md").symlink_to(self.root / "guide.md")
        manifest.write_text(json.dumps({"resources": [{**entry, "paths": {"en": "alias.md"}}]}))
        with patch.object(lr, "ROOT", self.root), patch.object(lr, "RESOURCES_FILE", manifest):
            self.assertEqual(lr.resources()[0]["path"], (self.root / "guide.md").resolve())
            self.assertEqual(lr.resources("fr")[0]["source_language"], "en")

    def test_malformed_manifests_fail_cleanly(self):
        manifest, entry = self.manifest()
        for bad in ({}, {"resources": {}}, {"resources": ["bad"]},
                    {"resources": [{**entry, "paths": []}]},
                    {"resources": [{**entry, "paths": {"en": 4}}]},
                    {"resources": [{**entry, "title": "not-map"}]},
                    {"resources": [entry, entry]}):
            manifest.write_text(json.dumps(bad))
            with self.subTest(data=bad), patch.object(lr, "RESOURCES_FILE", manifest):
                with self.assertRaises(SystemExit):
                    lr.resources()

    def test_opener_failure_codes_and_missing_binary_propagate(self):
        with patch.object(lr.sys, "platform", "linux"), contextlib.redirect_stderr(io.StringIO()):
            with patch.object(lr.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)):
                self.assertEqual(lr._open_resource("framework-guide", "en"), 7)
                self.assertEqual(ob.main(["onboard", "--open-resource", "framework-guide"]), 7)
            with patch.object(lr.subprocess, "run", side_effect=FileNotFoundError("xdg-open")):
                self.assertEqual(lr._open_resource("framework-guide", "en"), 1)

    def test_windows_uses_startfile_without_shell_and_catches_failure(self):
        with patch.object(lr.sys, "platform", "win32"), patch.object(lr.subprocess, "run") as run:
            with patch.object(lr.os, "startfile", create=True) as startfile:
                self.assertEqual(lr._open_resource("framework-guide", "en"), 0)
                startfile.assert_called_once()
                self.assertTrue(startfile.call_args.args[0].endswith("ecosystem.en.md"))
            with patch.object(lr.os, "startfile", None, create=True), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(lr._open_resource("framework-guide", "en"), 1)
            run.assert_not_called()

    def test_main_and_picker_use_same_opener_and_propagate_failure(self):
        with patch.object(ob, "_open_resource", return_value=6) as opened:
            self.assertEqual(ob.main(["onboard", "--open-resource", "framework-guide", "--language", "fr"]), 6)
            opened.assert_called_once_with("framework-guide", "fr")
            opened.reset_mock()
            with patch("builtins.input", side_effect=["R", "1"]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ob.picker([], None, "fr"), 6)
            opened.assert_called_once_with("framework-guide", "fr")

    def test_readonly_resource_routes_never_open(self):
        with patch.object(ob, "_open_resource") as onboard_open, \
             patch.object(lr, "_open_resource") as resource_open, \
             patch.object(lr.subprocess, "run") as process_open, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ob.main(["onboard", "--resources", "--json"]), 0)
            self.assertEqual(lr.main(["resources", "--json"]), 0)
            with patch("builtins.input", side_effect=["R", "b", "q"]):
                self.assertEqual(ob.picker([], None, "fr"), 0)
            onboard_open.assert_not_called()
            resource_open.assert_not_called()
            process_open.assert_not_called()


if __name__ == "__main__":
    unittest.main()
