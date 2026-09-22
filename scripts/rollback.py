#!/usr/bin/env python3
"""Restore instinct.md, profile-soul.md, and raw/ from rollback/last-good.

Wiki pages that are not in the snapshot are not deleted; if raw and the soul files are restored, the previous owner page stays as it was.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SKIP = {".env", "output", "wiki"}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: rollback.py <company-dir>", file=sys.stderr)
        return 2
    company = Path(argv[1])
    if not company.is_dir():
        print(f"not a directory: {company}", file=sys.stderr)
        return 2
    snap = company / "rollback" / "last-good"
    if not snap.is_dir():
        print("no snapshot", file=sys.stderr)
        return 2
    harvest = company / "raw" / "harvest.md"
    if harvest.is_file():
        failed = company / "rollback" / "failed-harvest.md"
        failed.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(harvest, failed)
    for path in snap.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(snap)
        if any(part in SKIP for part in rel.parts):
            continue
        dest = company / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
