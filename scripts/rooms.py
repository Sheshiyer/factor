#!/usr/bin/env python3
"""Room rules. A healthy numbers room sends nothing."""

from __future__ import annotations

import sys
from pathlib import Path


def numbers_message(crossed: bool) -> str | None:
    if not crossed:
        return None
    return "report"


def room_problems(root: Path) -> list[str]:
    found: list[str] = []
    content = root / "desks" / "content" / "brief.md"
    if content.is_file():
        text = content.read_text(encoding="utf-8")
        if "does not publish" not in text:
            found.append("content room can publish")
        if "Page:" not in text:
            found.append("content brief cites no page")
    numbers = root / "desks" / "numbers" / "report.md"
    if numbers.is_file():
        text = numbers.read_text(encoding="utf-8")
        if "## Figures" not in text or "## Suggestion" not in text:
            found.append("numbers report mixes the figure and the suggestion")
        if "Stay quiet" not in text:
            found.append("numbers room is not quiet")
        if "Page:" not in text:
            found.append("numbers figure has no page")
    for name in ("partners", "money"):
        path = root / "desks" / name / "playbook.md"
        if path.is_file() and "Do not send" not in path.read_text(encoding="utf-8"):
            found.append(f"{name} room can send")
    gates = root / "desks" / "gates.md"
    if gates.is_file():
        text = gates.read_text(encoding="utf-8")
        for gate in ("Send: wait", "Spend: wait", "Publish: wait", "0.85"):
            if gate not in text:
                found.append(f"gates missing {gate}")
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: rooms.py <company-dir>", file=sys.stderr)
        return 2
    found = room_problems(Path(argv[1]))
    if not found:
        print("rooms hold")
        return 0
    for item in found:
        print(item)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
