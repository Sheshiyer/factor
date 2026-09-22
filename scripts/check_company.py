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
    found.extend(money_problems(root))
    found.extend(length_problems(root))
    found.extend(wiki_problems(root))
    found.extend(fill_problems(root))
    return found


AMOUNT = re.compile(r"\$\d[\d,]*(?:\.\d+)?")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
SOUL_LINES = 80
INSTINCT_LINES = 40


def nonempty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def length_problems(root: Path) -> list[str]:
    found: list[str] = []
    soul = root / "profile-soul.md"
    if soul.is_file() and nonempty_lines(soul) > SOUL_LINES:
        found.append("profile soul exceeds 80 lines")
    instinct = root / "instinct.md"
    if instinct.is_file() and nonempty_lines(instinct) > INSTINCT_LINES:
        found.append("instinct exceeds 40 lines")
    return found


def wiki_problems(root: Path) -> list[str]:
    index = root / "wiki" / "index.md"
    if not index.is_file():
        return []
    stems = {path.stem for path in root.rglob("*.md") if path.is_file()}
    found: list[str] = []
    seen: set[str] = set()
    for name in WIKILINK.findall(index.read_text(encoding="utf-8")):
        if "/" in name or name in seen:
            continue
        seen.add(name)
        if name not in stems:
            found.append(f"missing wiki page {name}")
    return found


def fill_problems(root: Path) -> list[str]:
    output = root / "output"
    if not output.is_dir():
        return []
    found: list[str] = []
    for draft in output.glob("*.md"):
        if draft.name == "README.md":
            continue
        if UNFILLED in draft.read_text(encoding="utf-8"):
            found.append(f"FILL treated as fact in output/{draft.name}")
    return found


def money_problems(root: Path) -> list[str]:
    corpus_parts: list[str] = []
    for folder in ("context", "wiki", "brand"):
        base = root / folder
        if not base.is_dir():
            continue
        for path in base.rglob("*.md"):
            corpus_parts.append(path.read_text(encoding="utf-8"))
    corpus = "\n".join(corpus_parts)
    output = root / "output"
    if not output.is_dir():
        return []
    found: list[str] = []
    for draft in output.glob("*.md"):
        if draft.name == "README.md":
            continue
        for amount in AMOUNT.findall(draft.read_text(encoding="utf-8")):
            if amount not in corpus:
                found.append(f"unsourced amount {amount} in output/{draft.name}")
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
