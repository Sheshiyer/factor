import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "scripts" / "snapshot.py"
BACK = ROOT / "scripts" / "rollback.py"
LOG = ROOT / "scripts" / "debug_log.py"


class RollbackTest(unittest.TestCase):
    def test_redacts_secrets(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("debug_log", LOG)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        text = module.redact("sk-abc and ghp_abc and Bearer tok")
        self.assertNotIn("sk-abc", text)
        self.assertNotIn("ghp_abc", text)
        self.assertIn("[redacted]", text)

    def test_debug_log_refuses_unknown_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(LOG), tmp, "--intent", "i1", "--result", "maybe"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)

    def test_rollback_restores_instinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            (dest / "raw").mkdir()
            (dest / "raw" / "harvest.md").write_text("first\n", encoding="utf-8")
            (dest / "instinct.md").write_text("Ada\n", encoding="utf-8")
            (dest / "profile-soul.md").write_text("soul\n", encoding="utf-8")
            made = subprocess.run([sys.executable, str(SNAP), str(dest)], capture_output=True, text=True)
            self.assertEqual(made.returncode, 0, made.stderr)
            (dest / "instinct.md").write_text("changed\n", encoding="utf-8")
            (dest / "raw" / "harvest.md").write_text("second\n", encoding="utf-8")
            restored = subprocess.run([sys.executable, str(BACK), str(dest)], capture_output=True, text=True)
            self.assertEqual(restored.returncode, 0, restored.stderr)
            self.assertEqual((dest / "instinct.md").read_text(encoding="utf-8"), "Ada\n")
            self.assertEqual((dest / "rollback" / "failed-harvest.md").read_text(encoding="utf-8"), "second\n")

    def test_rollback_without_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(BACK), tmp],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("no snapshot", result.stderr)


if __name__ == "__main__":
    unittest.main()
