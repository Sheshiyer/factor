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

scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))
from preferences import load_language, save_language
from learning_resources import resources as _learning_resources, _open_resource, _format_text

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
LABELS_FR = {
    "skills": "Compétences",
    "plugins": "Plugins",
    "other": "Autres capacités",
}
STEPS_FR = """Intégration Factor
1. Récolte. Dans le projet que vous avez construit, collez prompts/harvest-claude.fr.md dans Claude, ou prompts/harvest-codex.fr.md dans Codex. Enregistrez la réponse sous le nom factor-harvest.md.
2. Appliquez. scripts/onboard.py --company <company> --apply-harvest <project>/factor-harvest.md
   Cela écrit SOUL.md, les six fichiers de contexte, et les dossiers business et brand. SOUL.md définit qui est le propriétaire et comment l'entreprise s'exprime.
3. Choisissez. Compétences, puis plugins, puis autres capacités.
4. Confirmez. python3 scripts/check_company.py <company>
"""
def labels(language: str) -> dict[str, str]:
    return LABELS_FR if language == "fr" else LABELS


def ui(english: str, french: str, language: str) -> str:
    return french if language == "fr" else english


def source_note(language: str) -> str:
    return ui("Source content: catalog names, descriptions and codes remain in their original language (English).",
              "Contenu source : les noms, descriptions et codes du catalogue restent dans leur langue d’origine (anglais).", language)


def load_items() -> list[dict[str, str]]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def by_category(items: list[dict[str, str]], category: str) -> list[dict[str, str]]:
    return [item for item in items if item["category"] == category]


def text_catalog(items: list[dict[str, str]], category: str | None, language: str = "en") -> str:
    chosen = items if category is None else by_category(items, category)
    lines: list[str] = [source_note(language), ""]
    groups = (category,) if category else CATEGORIES
    for group in groups:
        rows = [item for item in chosen if item["category"] == group]
        lines.append(labels(language)[group].upper())
        for disposition, title in (
            ("add", ui("offered", "proposés", language)),
            ("builtin", ui("already in Hermes", "déjà dans Hermes", language)),
            ("shelf", ui("not offered", "non proposés", language)),
        ):
            block = [item for item in rows if item["disposition"] == disposition]
            if not block:
                continue
            lines.append(f"  {title}")
            for item in block:
                repo = item["repo"] or ui("no repo in the cache", "aucun dépôt dans le cache", language)
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
    maybe_snapshot(company)


def maybe_snapshot(company: Path) -> None:
    import subprocess
    from check_company import problems

    if problems(company):
        return
    script = Path(__file__).resolve().parent / "snapshot.py"
    subprocess.run([sys.executable, str(script), str(company)], check=False)


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


def write_io_and_evals(company: Path) -> None:
    io = company / "io"
    io.mkdir(exist_ok=True)
    (io / "in.md").write_text(
        "# Job in\n\n"
        "A job arrives as one sentence from the Mac menu, Raycast, or Hermes.\n\n"
        "- Room. One of content, numbers, growth, ads, partners, money, or the desk the harvest named.\n"
        "- Sentence. The founder's words, unchanged.\n"
        "- Pages. Only the wiki lines the index matched. Do not attach the whole company.\n",
        encoding="utf-8",
    )
    (io / "out.md").write_text(
        "# Job out\n\n"
        "A finished job returns:\n\n"
        "- The draft path under `output/`.\n"
        "- The pages it read.\n"
        "- Every number it claims, and the page that number came from.\n"
        "- A yes or no on whether a person must see it, with a confidence from 0 to 1.\n\n"
        "A number with no page is a failed output. Under 0.5, ask Claude or the founder. "
        "Send, spend, and publish require an explicit founder approval record. "
        "Confidence alone cannot authorise an action. "
        "Jev may pick and score. It may not write the draft.\n",
        encoding="utf-8",
    )
    checks = company / "evals"
    checks.mkdir(exist_ok=True)
    (checks / "checks.md").write_text(
        "# Checks\n\n"
        "- Every figure in a draft under `output/` appears in `wiki/` or `context/`.\n"
        "- A line that still says `FILL:` is not a fact.\n"
        "- Send, spend, and publish require an explicit approval record from the founder.\n"
        "- Confidence alone cannot authorise a send, spend, or publish.\n\n"
        "Record the result in `wiki/log.md` as pass, fail, or could not tell.\n",
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
            "One row each time the founder rewrites a draft. The same reason twice proposes a voice rule for explicit founder review before acceptance.\n\n"
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
            "# Output\n\nDrafts and reports land here. Filed understanding goes back into `wiki/` or `brand/`.\n"
            "A number in a draft must already appear in `wiki/` or `context/`. Otherwise the draft does not ship.\n",
            encoding="utf-8",
        )
    write_io_and_evals(company)


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


def show_prompt(seat: str, language: str = "en") -> None:
    suffix = f".{language}" if language != "en" else ""
    path = PROMPTS / f"harvest-{seat}{suffix}.md"
    if not path.is_file():
        path = PROMPTS / f"harvest-{seat}.md"
    text = path.read_text(encoding="utf-8")
    print(text, end="" if text.endswith("\n") else "\n")


def picker(items: list[dict[str, str]], company: Path | None, language: str = "en") -> int:
    selected: set[str] = set()
    offered = [item for item in items if item["disposition"] == "add"]
    steps = STEPS_FR if language == "fr" else STEPS
    print(steps)
    while True:
        if language == "fr":
            print("\nIntégration Factor")
            if company:
                print(f"Entreprise : {company}")
            print("1  Afficher le prompt de récolte Claude")
            print("2  Afficher le prompt de récolte Codex")
            print("3  Appliquer un fichier de récolte (écrit SOUL.md)")
            print("4  Choisir les compétences, plugins et autres capacités")
            print("5  Afficher les quatre étapes")
            print("L  Basculer la langue (actuellement fr → en)")
            print("R  Afficher les ressources d'apprentissage")
            print("q  quitter")
        else:
            print("\nFactor onboarding")
            if company:
                print(f"Company: {company}")
            print("1  Show the Claude harvest prompt")
            print("2  Show the Codex harvest prompt")
            print("3  Apply a harvest file (writes SOUL.md)")
            print("4  Choose skills, plugins, and other capabilities")
            print("5  Show the four steps")
            print("L  Toggle language (currently en → fr)")
            print("R  Show learning resources")
            print("q  quit")
        choice = input("> ").strip()
        lower = choice.lower()
        if lower in {"q", "quit"}:
            break
        if lower == "l":
            language = "fr" if language == "en" else "en"
            if company is not None:
                save_language(company, language)
            steps = STEPS_FR if language == "fr" else STEPS
            print(steps)
            continue
        if lower == "r":
            res_list = _learning_resources(language)
            if not res_list:
                msg = "Aucune ressource disponible." if language == "fr" else "No resources available."
                print(msg)
                prompt = "entrée pour revenir " if language == "fr" else "enter to go back "
                input(prompt)
                continue
            while True:
                print()
                for idx, r in enumerate(res_list, start=1):
                    exists_mark = "" if r["path"].exists() else "  [fichier manquant]" if language == "fr" else "  [file missing]"
                    content_label = ui("content language", "langue du contenu", language)
                    print(f"  {idx}  [{r['kind']}]  {r['title']}{exists_mark}  ({content_label}: {r['source_language']})")
                if language == "fr":
                    print("numéro pour ouvrir une ressource, b pour revenir")
                    note = "Note : les résumés de registre restent en anglais."
                else:
                    print("number to open a resource, b to go back")
                    note = ""
                if note:
                    print(note)
                rchoice = input("> ").strip().lower()
                if rchoice == "b":
                    break
                if rchoice.isdigit() and 1 <= int(rchoice) <= len(res_list):
                    r = res_list[int(rchoice) - 1]
                    result = _open_resource(r["id"], language)
                    if result:
                        return result
                    continue
                bad = "Pas un choix sur cet écran." if language == "fr" else "Not a choice on this screen."
                print(bad)
            continue
        if lower == "1":
            show_prompt("claude", language)
            continue
        if lower == "2":
            show_prompt("codex", language)
            continue
        if lower == "3":
            if company is None:
                msg = "Démarrez l'intégration avec --company pour que la récolte ait un dossier." if language == "fr" else "Start onboarding with --company so the harvest has a home."
                print(msg)
                continue
            prompt_harvest = "chemin vers factor-harvest.md> " if language == "fr" else "path to factor-harvest.md> "
            harvest = input(prompt_harvest).strip()
            apply_harvest(company, Path(harvest))
            msg = f"écrit {company / 'SOUL.md'} et context/" if language == "fr" else f"wrote {company / 'SOUL.md'} and context/"
            print(msg)
            continue
        if lower == "5":
            print(steps)
            continue
        if lower != "4":
            bad = "Utilisez 1, 2, 3, 4, 5, L, R ou q." if language == "fr" else "Use 1, 2, 3, 4, 5, L, R, or q."
            print(bad)
            continue
        if not choose_capabilities(items, offered, selected, company, language):
            continue
    return 0


def choose_capabilities(
    items: list[dict[str, str]],
    offered: list[dict[str, str]],
    selected: set[str],
    company: Path | None,
    language: str = "en",
) -> bool:
    while True:
        print(ui("\nStep 3. Choose. q returns to the steps.", "\nÉtape 3. Choisissez. q revient aux étapes.", language))
        print(source_note(language))
        for index, category in enumerate(CATEGORIES, start=1):
            count = sum(1 for item in offered if item["category"] == category)
            chosen = sum(1 for item in offered if item["category"] == category and item["id"] in selected)
            print(f"  {index}  {labels(language)[category]}  ({chosen}/{count} " + ui("selected)", "sélectionnés)", language))
        print(ui("  4  Already in Hermes", "  4  Déjà dans Hermes", language))
        print(ui("  5  Not offered", "  5  Non proposés", language))
        choice = input("> ").strip().lower()
        if choice in {"q", "quit", "w", "write"}:
            break
        if choice in {"1", "2", "3"}:
            category = CATEGORIES[int(choice) - 1]
            if not toggle_category(offered, category, selected, language):
                continue
        elif choice == "4":
            show_fixed(items, "builtin", ui("Already in Hermes", "Déjà dans Hermes", language), language)
        elif choice == "5":
            show_fixed(items, "shelf", ui("Not offered", "Non proposés", language), language)
        else:
            print(ui("Use 1, 2, 3, 4, 5, or q.", "Utilisez 1, 2, 3, 4, 5 ou q.", language))
    chosen = [item for item in offered if item["id"] in selected]
    payload = [{"id": item["id"], "category": item["category"], "name": item["name"]} for item in chosen]
    print(json.dumps(payload, indent=2))
    if company:
        write_enabled(company, chosen)
        print(ui("wrote ", "écrit ", language) + str(company / "connectors" / "enabled.yaml"))
    return 0


def row_line(index: int, item: dict[str, str], selected: set[str], language: str = "en") -> str:
    mark = "x" if item["id"] in selected else " "
    repo = ui("repo", "dépôt", language) if item["repo"] else ui("no repo", "aucun dépôt", language)
    return (
        f"  {index:2} [{mark}] {item['id']}  {ui('risk', 'risque', language)} {item['risk']}  "
        f"{ui('approval', 'approbation', language)} {item['approval']}  {repo}  {item['summary']}"
    )


def show_detail(item: dict[str, str], language: str = "en") -> None:
    repo = item["repo"] or ui("no repository URL in the bookmark cache", "aucune URL de dépôt dans le cache de favoris", language)
    install = (
        f"npx skills add {item['repo']}"
        if item["repo"].startswith("https://github.com/")
        else ui("no install command until a repository URL exists", "aucune commande d’installation sans URL de dépôt", language)
    )
    print(f"\n{item['id']}  {item['name']}")
    print(f"  {labels(language)[item['category']]}  {item['kind']}  {ui('risk', 'risque', language)} {item['risk']}  {ui('approval', 'approbation', language)} {item['approval']}")
    print(source_note(language))
    print(f"  {item['summary']}")
    print(f"  {ui('bookmark', 'favori', language)} {item['bookmark']}")
    print(f"  {repo}")
    print(f"  {install}")


def toggle_category(offered: list[dict[str, str]], category: str, selected: set[str], language: str = "en") -> bool:
    rows = [item for item in offered if item["category"] == category]
    query = ""
    while True:
        visible = [
            item
            for item in rows
            if not query or query in item["id"] or query in item["summary"].lower()
        ]
        print(f"\n{labels(language)[category]}" + (f"  /{query}" if query else ""))
        for index, item in enumerate(visible, start=1):
            print(row_line(index, item, selected, language))
        print(ui("number toggles, d number details, /text filters, a all, c clear, b back", "numéro pour sélectionner, d numéro pour les détails, /texte pour filtrer, a tous, c effacer, b retour", language))
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
                show_detail(visible[number - 1], language)
            else:
                print(ui("Not a row on this screen.", "Aucune ligne correspondante sur cet écran.", language))
            continue
        if lowered.isdigit() and 1 <= int(lowered) <= len(visible):
            item_id = visible[int(lowered) - 1]["id"]
            if item_id in selected:
                selected.remove(item_id)
            else:
                selected.add(item_id)
            continue
        print(ui("Not a choice on this screen.", "Pas un choix sur cet écran.", language))


def show_fixed(items: list[dict[str, str]], disposition: str, title: str, language: str = "en") -> None:
    print(f"\n{title}")
    for item in items:
        if item["disposition"] != disposition:
            continue
        print(f"  {item['id']}  [{labels(language)[item['category']]}]  {item['summary']}")
    input(ui("enter to go back ", "entrée pour revenir ", language))


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
    parser.add_argument("--debug", action="store_true", help="append a redacted line to io/debug.log")
    parser.add_argument("--language", choices=("en", "fr"), help="language for this invocation (does not persist)")
    parser.add_argument("--set-language", choices=("en", "fr"), dest="set_language", help="persist language in company/preferences.json and exit unless other actions follow")
    parser.add_argument("--resources", action="store_true", help="display the learning resource list")
    parser.add_argument("--open-resource", metavar="ID", dest="open_resource", help="open a learning resource by ID")
    args = parser.parse_args(argv[1:])
    items = load_items()
    # Resolve effective language: --language > --set-language > company pref > default en
    if args.language:
        lang = args.language
    elif args.set_language:
        lang = args.set_language
    else:
        lang = load_language(args.company)

    if args.set_language:
        if args.company is None:
            raise SystemExit("--set-language needs --company")
        save_language(args.company, args.set_language)
        # Exit unless another explicit action was also requested
        has_other_action = bool(
            args.steps or args.prompt or args.apply_harvest
            or args.json or args.text or args.enable or args.enable_category
            or args.resources or args.open_resource
        )
        if not has_other_action:
            return 0
    if args.steps:
        steps_text = STEPS_FR if lang == "fr" else STEPS
        print(steps_text, end="" if steps_text.endswith("\n") else "\n")
        return 0
    if args.prompt:
        show_prompt(args.prompt, lang)
        return 0
    if args.open_resource:
        return _open_resource(args.open_resource, lang)
    if args.resources:
        res_list = _learning_resources(lang)
        if args.json:
            printable = [{"id": r["id"], "kind": r["kind"], "language": r["language"], "source_language": r["source_language"], "title": r["title"], "path": str(r["path"])} for r in res_list]
            print(json.dumps(printable, indent=2, ensure_ascii=False))
            return 0
        print(_format_text(res_list, lang))
        return 0
    if args.apply_harvest:
        if args.company is None:
            raise SystemExit("--apply-harvest needs --company")
        apply_harvest(args.company, args.apply_harvest)
        if args.debug:
            from check_company import problems
            from debug_log import append_log

            append_log(args.company, "apply", "fail" if problems(args.company) else "pass")
        print(ui("wrote ", "écrit ", lang) + str(args.company / "SOUL.md"))
        if not args.enable and not args.enable_category:
            return 0

    if args.json:
        rows = items if not args.category else by_category(items, args.category)
        print(json.dumps(rows, indent=2))
        return 0
    if args.text or (not sys.stdin.isatty() and not args.enable and not args.enable_category):
        if not args.text:
            print(STEPS_FR if lang == "fr" else STEPS)
        print(text_catalog(items, args.category, lang), end="")
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
            print(ui("wrote ", "écrit ", lang) + str(args.company / "connectors" / "enabled.yaml"), file=sys.stderr)
        return 0

    if not sys.stdin.isatty():
        print(text_catalog(items, args.category, lang), end="")
        return 0
    return picker(items, args.company, lang)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
