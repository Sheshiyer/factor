import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "scripts" / "write_intent.py"
CARD = ROOT / "scripts" / "intent_card.py"
RAY = ROOT / "surfaces" / "raycast" / "factor.sh"


def run_write(company: Path, sentence: str, room: str, door: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(WRITE), str(company), "--sentence", sentence, "--room", room, "--door", door],
        capture_output=True,
        text=True,
    )


class DoorTest(unittest.TestCase):
    def test_mac_and_hermes_share_card_fields(self):
        sentence = "Draft the weekday list."
        with tempfile.TemporaryDirectory() as tmp:
            company = Path(tmp)
            fields = []
            for door in ("mac", "hermes"):
                result = run_write(company, sentence, "content", door)
                self.assertEqual(result.returncode, 0, result.stderr)
                shown = subprocess.run(
                    [sys.executable, str(CARD), str(company / "io" / "intent.json")],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(shown.returncode, 0, shown.stderr)
                payload = json.loads(shown.stdout)
                self.assertEqual(
                    payload,
                    {
                        "desk": "content",
                        "seat": "claude",
                        "done": "A draft in output/ that cites the pages it read.",
                        "read": "instinct.md and the one wiki page the index matched.",
                        "write": "output/",
                    },
                )
                self.assertNotIn("door", payload)
                fields.append(payload)
            self.assertEqual(fields[0], fields[1])

    def test_raycast_arguments_become_the_intent(self):
        sentence = "What changed overnight."
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            company = Path(tmp) / "acme"
            company.mkdir()
            support = home / "Library" / "Application Support" / "Factor"
            support.mkdir(parents=True)
            (support / "company.path").write_text(str(company) + "\n", encoding="utf-8")
            env = os.environ.copy()
            env["HOME"] = str(home)
            result = subprocess.run(
                ["bash", str(RAY), sentence, "numbers"],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((company / "io" / "intent.json").read_text(encoding="utf-8"))
            self.assertEqual(
                payload,
                {"sentence": sentence, "room": "numbers", "door": "raycast"},
            )
            mode = RAY.stat().st_mode
            self.assertTrue(mode & stat.S_IXUSR)
