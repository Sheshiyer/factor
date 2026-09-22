#!/usr/bin/env python3
"""TUI and agent onboarding for the Factor catalog.

Agent use (no prompts):

    python3 scripts/onboard.py --json
    python3 scripts/onboard.py --text --category skills
    python3 scripts/onboard.py --company /path/to/company --enable openspec,ffmpeg-skill

A terminal runs the picker. A pipe prints the catalog and does not wait.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "connectors" / "registry.json"
CARDS = ROOT / "catalog" / "cards"
PROMPTS = ROOT / "prompts"
HARVEST_SECTIONS = (
    "owner",
    "soul",
    "company",
    "customer",
    "offer",
    "positioning",
    "voice",
    "proof",
)
STEPS = """Factor onboarding
1. Harvest. In the project you have been building, paste prompts/harvest-claude.md into Claude, or prompts/harvest-codex.md into Codex. Save the reply as factor-harvest.md.
2. Apply. scripts/onboard.py --company <company> --apply-harvest <project>/factor-harvest.md
   This writes SOUL.md, the six context files, and the business and brand folders. SOUL.md is who the owner is and how the business sounds.
3. Choose. Skills, then plugins, then other capabilities.
4. Confirm. python3 scripts/check_company.py <company>
"""
CATEGORIES = ("skills", "plugins", "other")
LABELS = {
    "skills": "Skills",
    "plugins": "Plugins",
    "other": "Other capabilities",
}


def load_items() -> list[dict[str, str]]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def by_category(items: list[dict[str, str]], category: str) -> list[dict[str, str]]:
    return [item for item in items if item["category"] == category]


def text_catalog(items: list[dict[str, str]], category: str | None) -> str:
    chosen = items if category is None else by_category(items, category)
    lines: list[str] = []
    groups = (category,) if category else CATEGORIES
    for group in groups:
        rows = [item for item in chosen if item["category"] == group]
        lines.append(LABELS[group].upper())
        for disposition, title in (
            ("add", "offered"),
            ("builtin", "already in Hermes"),
            ("shelf", "not offered"),
        ):
            block = [item for item in rows if item["disposition"] == disposition]
            if not block:
                continue
            lines.append(f"  {title}")
            for item in block:
                repo = item["repo"] or "no repo in the cache"
                lines.append(
                    f"  - {item['id']} | {item['name']} | {item['kind']} | {item['risk']} | {repo}"
                )
                lines.append(f"    {item['summary']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def copy_cards(company: Path, chosen: list[dict[str, str]]) -> None:
    chosen_ids = {item["id"] for item in chosen}
    offered = {path.name for path in CARDS.iterdir() if path.is_dir()} if CARDS.is_dir() else set()
    skills = company / "skills"
    if skills.is_dir():
        for child in skills.iterdir():
            if not child.is_dir() or child.name not in offered or child.name in chosen_ids:
                continue
            card = child / "SKILL.md"
            if card.is_file():
                card.unlink()
            if not any(child.iterdir()):
                child.rmdir()
    for item in chosen:
        source = CARDS / item["id"] / "SKILL.md"
        if not source.is_file():
            raise SystemExit(f"missing catalog card: {item['id']}")
        dest = company / "skills" / item["id"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SKILL.md").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def write_enabled(company: Path, chosen: list[dict[str, str]]) -> None:
    target = company / "connectors" / "enabled.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "version: 1",
        "# Written by scripts/onboard.py. Credentials do not go in this file.",
        "connectors:",
    ]
    if not chosen:
        lines = [
            "version: 1",
            "# Written by scripts/onboard.py. Credentials do not go in this file.",
            "connectors: []",
        ]
    else:
        for item in chosen:
            lines.append(f"  - id: {item['id']}")
            lines.append(f"    category: {item['category']}")
            lines.append(f"    kind: {item['kind']}")
            lines.append(f"    risk: {item['risk']}")
            lines.append(f"    approval: {item['approval']}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    copy_cards(company, chosen)


def harvest_sections(text: str) -> dict[str, str]:
    current: str | None = None
    buckets: dict[str, list[str]] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            buckets.setdefault(current, [])
            continue
        if current:
            buckets[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in buckets.items()}


def apply_harvest(company: Path, harvest: Path) -> None:
    if not harvest.is_file():
        raise SystemExit(f"harvest file not found: {harvest}")
    sections = harvest_sections(harvest.read_text(encoding="utf-8"))
    missing = [name for name in HARVEST_SECTIONS if name not in sections]
    if missing:
        raise SystemExit("harvest is missing headings: " + ", ".join(missing))
    company.mkdir(parents=True, exist_ok=True)
    (company / "context").mkdir(exist_ok=True)
    soul = sections["soul"] or "FILL: the harvest left the soul blank."
    owner = sections["owner"] or "FILL: the harvest left the owner blank."
    (company / "SOUL.md").write_text(
        "# Soul\n\n"
        "Paste `profile-soul.md` into the Hermes profile. That file is what Hermes reads on every turn. "
        "Keep it to identity, voice, and refusals. The business lives in `wiki/` and `brand/`.\n\n"
        f"{soul}\n\n## Owner\n\n{owner}\n",
        encoding="utf-8",
    )
    (company / "profile-soul.md").write_text(
        soul if soul.lstrip().startswith("#") else f"# Soul\n\n{soul}\n",
        encoding="utf-8",
    )
    write_instinct(company, soul, sections)
    titles = {
        "company": "Company",
        "customer": "Customer",
        "offer": "Offer",
        "positioning": "Positioning",
        "voice": "Voice",
        "proof": "Proof",
    }
    for key, title in titles.items():
        body = sections[key] or f"FILL: the harvest left {key} blank."
        (company / "context" / f"{key}.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    write_business_and_brand(company, sections, harvest)


def write_instinct(company: Path, soul: str, sections: dict[str, str]) -> None:
    stays = sections.get("stays", "").strip() or "FILL: nothing is locked yet."
    dna = one_line(sections.get("style dna", ""))
    (company / "instinct.md").write_text(
        "# Instinct\n\n"
        "Load this every time. It is small on purpose. The company memory is the wiki, and it stays on disk.\n\n"
        "## Who\n\n"
        f"{one_line(soul)}\n\n"
        "## Voice\n\n"
        f"{dna}\n\n"
        "## Locked\n\n"
        f"{stays}\n\n"
        "Hermes session memory is a scratch pad. Do not copy these pages into it.\n",
        encoding="utf-8",
    )


def write_desk(company: Path, desk: str) -> None:
    text = desk.strip()
    if not text or text.upper().startswith("FILL"):
        return
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = lines[0]
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")
    slug = "-".join(part for part in slug.split("-") if part)[:40] or "desk"
    scope = "\n".join(lines[1:]).strip() or "FILL: the harvest did not state the scope."
    folder = company / "departments" / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "playbook.md").write_text(
        f"# {name}\n\n"
        "This is the one desk the harvest named. Other desks wait.\n\n"
        f"## Scope\n\n{scope}\n\n"
        "## Heartbeat\n\n"
        "Stay quiet unless a card for this desk is blocked or waiting on review.\n",
        encoding="utf-8",
    )


def one_line(body: str) -> str:
    for line in body.splitlines():
        text = line.strip()
        if text:
            return text[:120]
    return "FILL: empty"


def page(title: str, body: str, source: str) -> str:
    text = body.strip() or f"FILL: nothing harvested for {title.lower()}."
    return (
        f"# {title}\n\n"
        f"Source: `{source}`. That file is the archive. Update this page when the understanding changes, "
        f"and append a line to `wiki/log.md`.\n\n"
        f"{text}\n"
    )


def write_business_and_brand(company: Path, sections: dict[str, str], harvest: Path) -> None:
    """Turn harvested context into a business wiki and a brand folder.

    The shape follows a second-brain vault: raw sources stay untouched,
    wiki/index.md is the catalog to read first, and brand pages hold
    voice, proof, and what is locked.
    """
    raw = company / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "harvest.md").write_text(harvest.read_text(encoding="utf-8"), encoding="utf-8")
    (raw / "README.md").write_text(
        "# Raw\n\nSources land here and are not edited after they land.\n",
        encoding="utf-8",
    )

    entities = company / "wiki" / "entities"
    concepts = company / "wiki" / "concepts"
    entities.mkdir(parents=True, exist_ok=True)
    concepts.mkdir(parents=True, exist_ok=True)
    brand = company / "brand"
    brand.mkdir(parents=True, exist_ok=True)

    pages = {
        entities / "owner.md": ("Owner", sections.get("owner", "")),
        entities / "company.md": ("Company", sections.get("company", "")),
        concepts / "customer.md": ("Customer", sections.get("customer", "")),
        concepts / "offer.md": ("Offer", sections.get("offer", "")),
        concepts / "positioning.md": ("Positioning", sections.get("positioning", "")),
        brand / "voice.md": ("Voice", sections.get("voice", "")),
        brand / "proof.md": ("Proof", sections.get("proof", "")),
    }
    for path, (title, body) in pages.items():
        path.write_text(page(title, body, "raw/harvest.md"), encoding="utf-8")

    lock_parts = []
    if sections.get("lock", "").strip():
        lock_parts.append(sections["lock"].strip())
    if sections.get("stays", "").strip():
        lock_parts.append("## Stays\n\n" + sections["stays"].strip())
    if sections.get("may change", "").strip():
        lock_parts.append("## May change\n\n" + sections["may change"].strip())
    lock = "\n\n".join(lock_parts).strip()
    if lock:
        (brand / "lock.md").write_text(f"# Lock\n\n{lock}\n", encoding="utf-8")
    else:
        (brand / "lock.md").write_text(
            "# Lock\n\n"
            "What the brand must keep, and what a later draft is allowed to change.\n\n"
            "## Stays\n\n"
            "FILL: the harvest did not name what must stay.\n\n"
            "## May change\n\n"
            "FILL: the harvest did not name what a draft may change.\n",
            encoding="utf-8",
        )
    dna = sections.get("style dna", "").strip()
    (brand / "style-dna.md").write_text(
        "# Style DNA\n\n"
        "Measured from the owner's own samples. A draft matches these numbers, or it does not ship.\n\n"
        + (dna or "FILL: the harvest did not measure a sample.\n"),
        encoding="utf-8",
    )
    write_desk(company, sections.get("desk", ""))
    corrections = company / "wiki" / "corrections.md"
    if not corrections.exists():
        corrections.write_text(
            "# Corrections\n\n"
            "One row each time the founder rewrites a draft. The same reason twice becomes a voice rule.\n\n"
            "| Original | Rewrite | Reason |\n"
            "| --- | --- | --- |\n",
            encoding="utf-8",
        )

    index = company / "wiki" / "index.md"
    index.write_text(
        "# Index\n\n"
        "Read this first. Open a page only when its line matches the work.\n\n"
        f"The owner, [[owner]], runs [[company]]. {one_line(sections.get('company', ''))}\n\n"
        f"The customer is [[customer]]. {one_line(sections.get('customer', ''))}\n\n"
        f"The offer is [[offer]]. {one_line(sections.get('offer', ''))}\n\n"
        f"The position is [[positioning]]. {one_line(sections.get('positioning', ''))}\n\n"
        f"The brand sounds like [[voice]]. {one_line(sections.get('voice', ''))}\n\n"
        "Claims live in [[proof]]. What stays locked is [[lock]].\n\n"
        "Sources stay in `raw/` and are not edited after they land. "
        "A synthesis page belongs in `wiki/synthesis/` only when it says something no source said.\n",
        encoding="utf-8",
    )
    (company / "wiki" / "synthesis").mkdir(exist_ok=True)
    synthesis_readme = company / "wiki" / "synthesis" / "README.md"
    if not synthesis_readme.exists():
        synthesis_readme.write_text(
            "# Synthesis\n\n"
            "Pages here say something no single source said. Leave this folder empty until that is true.\n",
            encoding="utf-8",
        )

    log = company / "wiki" / "log.md"
    line = "- structure written from raw/harvest.md\n"
    if log.exists():
        prior = log.read_text(encoding="utf-8")
        if line not in prior:
            log.write_text(prior.rstrip() + "\n" + line, encoding="utf-8")
    else:
        log.write_text("# Log\n\n" + line, encoding="utf-8")

    template_dir = company / "templates"
    template_dir.mkdir(exist_ok=True)
    (template_dir / "entity.md").write_text(
        "# Name\n\nSource: `raw/....md`\n\nOne entity. People, organisations, products, tools.\n",
        encoding="utf-8",
    )
    (template_dir / "concept.md").write_text(
        "# Name\n\nSource: `raw/....md`\n\nOne idea. Link it from `wiki/index.md` in a sentence.\n",
        encoding="utf-8",
    )
    output = company / "output"
    output.mkdir(exist_ok=True)
    output_readme = output / "README.md"
    if not output_readme.exists():
        output_readme.write_text(
            "# Output\n\nDrafts and reports land here. Filed understanding goes back into `wiki/` or `brand/`.\n",
            encoding="utf-8",
        )


def resolve_enable(items: list[dict[str, str]], raw: str) -> list[dict[str, str]]:
    wanted = [part.strip() for part in raw.split(",") if part.strip()]
    found: list[dict[str, str]] = []
    by_id = {item["id"]: item for item in items}
    for name in wanted:
        item = by_id.get(name)
        if item is None:
            raise SystemExit(f"unknown id: {name}")
        if item["disposition"] != "add":
            raise SystemExit(f"{name} is {item['disposition']} and cannot be enabled")
        found.append(item)
    return found


def show_prompt(seat: str) -> None:
    path = PROMPTS / f"harvest-{seat}.md"
    print(path.read_text(encoding="utf-8"), end="" if path.read_text(encoding="utf-8").endswith("\n") else "\n")


def picker(items: list[dict[str, str]], company: Path | None) -> int:
    selected: set[str] = set()
    offered = [item for item in items if item["disposition"] == "add"]
    print(STEPS)
    while True:
        print("\nFactor onboarding")
        if company:
            print(f"Company: {company}")
        print("1  Show the Claude harvest prompt")
        print("2  Show the Codex harvest prompt")
        print("3  Apply a harvest file (writes SOUL.md)")
        print("4  Choose skills, plugins, and other capabilities")
        print("5  Show the four steps")
        print("q  quit")
        choice = input("> ").strip().lower()
        if choice in {"q", "quit"}:
            break
        if choice == "1":
            show_prompt("claude")
            continue
        if choice == "2":
            show_prompt("codex")
            continue
        if choice == "3":
            if company is None:
                print("Start onboarding with --company so the harvest has a home.")
                continue
            harvest = input("path to factor-harvest.md> ").strip()
            apply_harvest(company, Path(harvest))
            print(f"wrote {company / 'SOUL.md'} and context/")
            continue
        if choice == "5":
            print(STEPS)
            continue
        if choice != "4":
            print("Use 1, 2, 3, 4, 5, or q.")
            continue
        if not choose_capabilities(items, offered, selected, company):
            continue
    return 0


def choose_capabilities(
    items: list[dict[str, str]],
    offered: list[dict[str, str]],
    selected: set[str],
    company: Path | None,
) -> bool:
    while True:
        print("\nStep 3. Choose. q returns to the steps.")
        for index, category in enumerate(CATEGORIES, start=1):
            count = sum(1 for item in offered if item["category"] == category)
            chosen = sum(1 for item in offered if item["category"] == category and item["id"] in selected)
            print(f"  {index}  {LABELS[category]}  ({chosen}/{count} selected)")
        print("  4  Already in Hermes")
        print("  5  Not offered")
        choice = input("> ").strip().lower()
        if choice in {"q", "quit", "w", "write"}:
            break
        if choice in {"1", "2", "3"}:
            category = CATEGORIES[int(choice) - 1]
            if not toggle_category(offered, category, selected):
                continue
        elif choice == "4":
            show_fixed(items, "builtin", "Already in Hermes")
        elif choice == "5":
            show_fixed(items, "shelf", "Not offered")
        else:
            print("Use 1, 2, 3, 4, 5, or q.")
    chosen = [item for item in offered if item["id"] in selected]
    payload = [{"id": item["id"], "category": item["category"], "name": item["name"]} for item in chosen]
    print(json.dumps(payload, indent=2))
    if company:
        write_enabled(company, chosen)
        print(f"wrote {company / 'connectors' / 'enabled.yaml'}")
    return 0


def row_line(index: int, item: dict[str, str], selected: set[str]) -> str:
    mark = "x" if item["id"] in selected else " "
    repo = "repo" if item["repo"] else "no repo"
    return (
        f"  {index:2} [{mark}] {item['id']}  risk {item['risk']}  "
        f"approval {item['approval']}  {repo}  {item['summary']}"
    )


def show_detail(item: dict[str, str]) -> None:
    repo = item["repo"] or "no repository URL in the bookmark cache"
    install = (
        f"npx skills add {item['repo']}"
        if item["repo"].startswith("https://github.com/")
        else "no install command until a repository URL exists"
    )
    print(f"\n{item['id']}  {item['name']}")
    print(f"  {LABELS[item['category']]}  {item['kind']}  risk {item['risk']}  approval {item['approval']}")
    print(f"  {item['summary']}")
    print(f"  bookmark {item['bookmark']}")
    print(f"  {repo}")
    print(f"  {install}")


def toggle_category(offered: list[dict[str, str]], category: str, selected: set[str]) -> bool:
    rows = [item for item in offered if item["category"] == category]
    query = ""
    while True:
        visible = [
            item
            for item in rows
            if not query or query in item["id"] or query in item["summary"].lower()
        ]
        print(f"\n{LABELS[category]}" + (f"  /{query}" if query else ""))
        for index, item in enumerate(visible, start=1):
            print(row_line(index, item, selected))
        print("number toggles, d number details, /text filters, a all, c clear, b back")
        choice = input("> ").strip()
        lowered = choice.lower()
        if lowered == "b":
            return True
        if lowered == "a":
            for item in visible:
                selected.add(item["id"])
            continue
        if lowered == "c":
            for item in visible:
                selected.discard(item["id"])
            continue
        if choice.startswith("/"):
            query = choice[1:].strip().lower()
            continue
        if lowered.startswith("d ") and lowered[2:].strip().isdigit():
            number = int(lowered[2:].strip())
            if 1 <= number <= len(visible):
                show_detail(visible[number - 1])
            else:
                print("Not a row on this screen.")
            continue
        if lowered.isdigit() and 1 <= int(lowered) <= len(visible):
            item_id = visible[int(lowered) - 1]["id"]
            if item_id in selected:
                selected.remove(item_id)
            else:
                selected.add(item_id)
            continue
        print("Not a choice on this screen.")


def show_fixed(items: list[dict[str, str]], disposition: str, title: str) -> None:
    print(f"\n{title}")
    for item in items:
        if item["disposition"] != disposition:
            continue
        print(f"  {item['id']}  [{LABELS[item['category']]}]  {item['summary']}")
    input("enter to go back ")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Factor catalog onboarding")
    parser.add_argument("--json", action="store_true", help="print the registry as JSON")
    parser.add_argument("--text", action="store_true", help="print a plain catalog for an agent")
    parser.add_argument("--category", choices=CATEGORIES)
    parser.add_argument("--company", type=Path, help="company repo whose enabled.yaml to write")
    parser.add_argument("--enable", help="comma-separated ids to enable")
    parser.add_argument("--enable-category", choices=CATEGORIES, help="enable every offered item in one category")
    parser.add_argument("--steps", action="store_true", help="print the four onboarding steps")
    parser.add_argument("--prompt", choices=("claude", "codex"), help="print the harvest prompt to copy")
    parser.add_argument("--apply-harvest", type=Path, help="write SOUL.md and context files from a harvest")
    args = parser.parse_args(argv[1:])
    items = load_items()

    if args.steps:
        print(STEPS, end="" if STEPS.endswith("\n") else "\n")
        return 0
    if args.prompt:
        show_prompt(args.prompt)
        return 0
    if args.apply_harvest:
        if args.company is None:
            raise SystemExit("--apply-harvest needs --company")
        apply_harvest(args.company, args.apply_harvest)
        print(f"wrote {args.company / 'SOUL.md'}")
        if not args.enable and not args.enable_category:
            return 0

    if args.json:
        rows = items if not args.category else by_category(items, args.category)
        print(json.dumps(rows, indent=2))
        return 0
    if args.text or (not sys.stdin.isatty() and not args.enable and not args.enable_category):
        if not args.text:
            print(STEPS)
        print(text_catalog(items, args.category), end="")
        if not args.enable and not args.enable_category:
            return 0

    chosen: list[dict[str, str]] = []
    if args.enable:
        chosen.extend(resolve_enable(items, args.enable))
    if args.enable_category:
        chosen.extend(
            item
            for item in items
            if item["category"] == args.enable_category and item["disposition"] == "add"
        )
    if args.enable or args.enable_category:
        # unique, registry order
        wanted = {item["id"] for item in chosen}
        chosen = [item for item in items if item["id"] in wanted]
        print(json.dumps([{"id": item["id"], "category": item["category"]} for item in chosen], indent=2))
        if args.company:
            write_enabled(args.company, chosen)
            print(f"wrote {args.company / 'connectors' / 'enabled.yaml'}", file=sys.stderr)
        return 0

    if not sys.stdin.isatty():
        print(text_catalog(items, args.category), end="")
        return 0
    return picker(items, args.company)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
