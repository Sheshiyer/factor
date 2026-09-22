#!/usr/bin/env python3
"""Report a Factor company repo that is still a blank glove."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "connectors" / "registry.json"

REQUIRED = (
    "AGENTS.md",
    "SOUL.md",
    "context/company.md",
    "context/customer.md",
    "context/offer.md",
    "context/positioning.md",
    "context/voice.md",
    "context/proof.md",
    "connectors/enabled.yaml",
)

UNFILLED = "FILL:"
UNNAMED = "__COMPANY__"


def problems(root: Path) -> list[str]:
    found: list[str] = []
    for rel in REQUIRED:
        path = root / rel
        if not path.is_file():
            found.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if UNNAMED in text:
            found.append(f"unnamed {rel}")
        if rel != "context/proof.md" and UNFILLED in text:
            found.append(f"unfilled {rel}")
    found.extend(enabled_problems(root))
    return found


def enabled_ids(text: str) -> list[str]:
    if re.search(r"(?m)^connectors:\s*\[\s*\]\s*$", text):
        return []
    return re.findall(r"(?m)^\s*-\s+id:\s*([A-Za-z0-9-]+)\s*$", text)


def enabled_problems(root: Path) -> list[str]:
    path = root / "connectors" / "enabled.yaml"
    if not path.is_file() or not REGISTRY.is_file():
        return []
    registry = {item["id"]: item for item in json.loads(REGISTRY.read_text(encoding="utf-8"))}
    found: list[str] = []
    for name in enabled_ids(path.read_text(encoding="utf-8")):
        item = registry.get(name)
        if item is None:
            found.append(f"unknown connector {name}")
        elif item["disposition"] != "add":
            found.append(f"connector {name} is {item['disposition']}")
        elif not (root / "skills" / name / "SKILL.md").is_file():
            found.append(f"missing card skills/{name}/SKILL.md")
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_company.py <company-dir>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    found = problems(root)
    if not found:
        print(f"{root} is filled")
        return 0
    print(f"{root} is still a blank glove:")
    for item in found:
        print(f"  {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
