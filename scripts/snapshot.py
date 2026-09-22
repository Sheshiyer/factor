#!/usr/bin/env python3
"""Copy instinct.md, profile-soul.md, and raw/ into rollback/last-good.

output/, wiki/, and .env are not copied.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REQUIRED = ("instinct.md", "profile-soul.md")
SKIP = {".env", "output", "wiki"}


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in SKIP}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: snapshot.py <company-dir>", file=sys.stderr)
        return 2
    company = Path(argv[1])
    if not company.is_dir():
        print(f"not a directory: {company}", file=sys.stderr)
        return 2
    missing = [name for name in REQUIRED if not (company / name).is_file()]
    if missing:
        print("missing " + ", ".join(missing), file=sys.stderr)
        return 2
    dest = company / "rollback" / "last-good"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for name in REQUIRED:
        shutil.copy2(company / name, dest / name)
    raw = company / "raw"
    if raw.is_dir():
        shutil.copytree(raw, dest / "raw", ignore=_ignore)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
