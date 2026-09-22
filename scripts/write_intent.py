#!/usr/bin/env python3
"""Write one intent into a company io folder. No wiki body."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOMS = ("content", "numbers", "growth", "ads", "partners", "money")
DOORS = ("mac", "raycast", "hermes")
USAGE = (
    "usage: write_intent.py <company-dir> "
    "--sentence TEXT --room ROOM --door mac|raycast|hermes"
)


def main(argv: list[str]) -> int:
    parsed = parse(argv[1:])
    if isinstance(parsed, int):
        return parsed
    company, sentence, room, door = parsed
    if room not in ROOMS:
        print("unknown room", file=sys.stderr)
        return 2
    if door not in DOORS:
        print("unknown door", file=sys.stderr)
        return 2
    if not company.is_dir():
        print(f"not a directory: {company}", file=sys.stderr)
        return 2
    try:
        commit(company, sentence, room, door)
    except OSError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


def parse(
    args: list[str],
) -> tuple[Path, str, str, str] | int:
    if not args or args[0].startswith("-"):
        print(USAGE, file=sys.stderr)
        return 2
    company = Path(args[0])
    sentence: str | None = None
    room: str | None = None
    door: str | None = None
    index = 1
    while index < len(args):
        flag = args[index]
        if flag not in ("--sentence", "--room", "--door"):
            print(USAGE, file=sys.stderr)
            return 2
        if index + 1 >= len(args):
            print(USAGE, file=sys.stderr)
            return 2
        value = args[index + 1]
        if flag == "--sentence":
            sentence = value
        elif flag == "--room":
            room = value
        else:
            door = value
        index += 2
    if sentence is None or room is None or door is None:
        print(USAGE, file=sys.stderr)
        return 2
    return company, sentence, room, door


def commit(company: Path, sentence: str, room: str, door: str) -> None:
    io = company / "io"
    io.mkdir(parents=True, exist_ok=True)
    temporary = io / "intent.json.new"
    target = io / "intent.json"
    payload = {"sentence": sentence, "room": room, "door": door}
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, target)
    (io / "status.txt").write_text("waiting", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
