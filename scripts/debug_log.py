#!/usr/bin/env python3
"""Append one redacted line to a company io/debug.log."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED = ("pass", "fail", "could-not-tell")

_TOKEN = re.compile(
    r"Bearer\s+\S+"
    r"|api_key\s*=\s*\S+"
    r"|sk-[A-Za-z0-9_+/=-]+"
    r"|ghp_[A-Za-z0-9_+/=-]+",
    re.IGNORECASE,
)


def redact(text: str) -> str:
    """Replace token-looking strings with [redacted]."""
    return _TOKEN.sub("[redacted]", text)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="debug_log.py",
        usage="%(prog)s <company-dir> --intent ID --result pass|fail|could-not-tell",
    )
    parser.add_argument("company")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args(argv[1:])
    if args.result not in ALLOWED:
        print("result must be pass, fail, or could-not-tell", file=sys.stderr)
        return 2
    company = Path(args.company)
    if not company.is_dir():
        print(f"not a directory: {company}", file=sys.stderr)
        return 2
    intent = args.intent.replace("\r", " ").replace("\n", " ")
    log = company / "io" / "debug.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    line = redact(f"intent={intent} result={args.result}")
    with log.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
