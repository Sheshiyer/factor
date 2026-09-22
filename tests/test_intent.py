import contextlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "scripts" / "write_intent.py"


def load_write_intent():
    spec = importlib.util.spec_from_file_location("factor_write_intent", WRITE)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_write(company: Path, sentence: str, room: str, door: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(WRITE),
            str(company),
            "--sentence",
            sentence,
            "--room",
            room,
            "--door",
            door,
        ],
        capture_output=True,
        text=True,
    )


class IntentTest(unittest.TestCase):
    def test_golden_sentence_room_and_door(self):
        sentence = "Draft the weekday list."
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "acme"
            company.mkdir()
            for door in ("mac", "raycast", "hermes"):
                result = run_write(company, sentence, "content", door)
                self.assertEqual(result.returncode, 0, result.stderr)
                intent = company / "io" / "intent.json"
                payload = json.loads(intent.read_text(encoding="utf-8"))
                self.assertEqual(
                    payload,
                    {"sentence": sentence, "room": "content", "door": door},
                )
                self.assertEqual(list(payload), ["sentence", "room", "door"])
                self.assertNotIn("wiki", intent.read_text(encoding="utf-8"))
                status = (company / "io" / "status.txt").read_text(encoding="utf-8")
                self.assertEqual(status.strip(), "waiting")
                self.assertNotIn(" ", status)
                self.assertFalse((company / "io" / "intent.json.new").exists())

    def test_unknown_room_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "acme"
            io = company / "io"
            io.mkdir(parents=True)
            intent = io / "intent.json"
            original = '{"sentence": "keep", "room": "content", "door": "mac"}\n'
            intent.write_text(original, encoding="utf-8")
            result = run_write(company, "Nope.", "kitchen", "mac")
            self.assertEqual(result.returncode, 2)
            self.assertIn("unknown room", result.stderr)
            self.assertEqual(intent.read_text(encoding="utf-8"), original)
            self.assertFalse((io / "intent.json.new").exists())

    def test_second_write_replaces_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "acme"
            company.mkdir()
            first = run_write(company, "First sentence.", "content", "mac")
            self.assertEqual(first.returncode, 0, first.stderr)
            intent = company / "io" / "intent.json"
            (company / "io" / "intent.json.new").write_text("stale", encoding="utf-8")
            second = run_write(company, "Second sentence.", "numbers", "hermes")
            self.assertEqual(second.returncode, 0, second.stderr)
            payload = json.loads(intent.read_text(encoding="utf-8"))
            self.assertEqual(
                payload,
                {
                    "sentence": "Second sentence.",
                    "room": "numbers",
                    "door": "hermes",
                },
            )
            self.assertNotIn("First sentence.", intent.read_text(encoding="utf-8"))
            names = sorted(path.name for path in (company / "io").iterdir())
            self.assertEqual(names, ["intent.json", "status.txt"])
            self.assertFalse((company / "io" / "intent.json.new").exists())

    def test_failed_replace_keeps_the_previous_intent(self):
        module = load_write_intent()
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp) / "acme"
            io = company / "io"
            io.mkdir(parents=True)
            intent = io / "intent.json"
            original = '{"sentence": "keep", "room": "content", "door": "mac"}\n'
            intent.write_text(original, encoding="utf-8")
            (io / "status.txt").write_text("ready", encoding="utf-8")

            def fail_replace(src, dst):
                raise OSError("replace failed")

            with mock.patch.object(module.os, "replace", side_effect=fail_replace):
                with contextlib.redirect_stderr(StringIO()):
                    code = module.main(
                        [
                            "write_intent.py",
                            str(company),
                            "--sentence",
                            "replace me",
                            "--room",
                            "numbers",
                            "--door",
                            "hermes",
                        ]
                    )
            self.assertEqual(code, 1)
            self.assertEqual(intent.read_text(encoding="utf-8"), original)
            self.assertEqual((io / "status.txt").read_text(encoding="utf-8"), "ready")
            self.assertTrue((io / "intent.json.new").is_file())


if __name__ == "__main__":
    unittest.main()
