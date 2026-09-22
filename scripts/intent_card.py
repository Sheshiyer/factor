#!/usr/bin/env python3
"""Turn an intent file into the five card fields. The door is not a field."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def card_fields(payload: dict) -> dict[str, str]:
    return {
        "desk": payload["room"],
        "seat": "claude",
        "done": "A draft in output/ that cites the pages it read.",
        "read": "instinct.md and the one wiki page the index matched.",
        "write": "output/",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: intent_card.py <intent.json>", file=sys.stderr)
        return 2
    payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(card_fields(payload), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
