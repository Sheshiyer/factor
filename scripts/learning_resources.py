#!/usr/bin/env python3
"""Learning resource helper for the Factor onboarding flow.

API
---
    resources(language)  -> list of dicts with id, kind, language, title, path

CLI
---
    python3 scripts/learning_resources.py [--language en|fr] [--company PATH]
    python3 scripts/learning_resources.py --json
    python3 scripts/learning_resources.py --open ID
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_FILE = ROOT / "docs" / "resources.json"


def _load_raw() -> dict:
    try:
        data = json.loads(RESOURCES_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"cannot read resources.json: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("resources"), list):
        raise SystemExit("resources.json must contain a resources list")
    seen = set()
    for entry in data["resources"]:
        if not isinstance(entry, dict):
            raise SystemExit("resources.json entries must be objects")
        identity = entry.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            raise SystemExit("resources.json requires unique nonempty resource IDs")
        seen.add(identity)
        for key in ("paths", "title"):
            mapping = entry.get(key)
            if not isinstance(mapping, dict) or not mapping or any(
                language not in ("en", "fr") or not isinstance(value, str) or not value.strip()
                for language, value in mapping.items()
            ):
                raise SystemExit(f"resource {identity}: {key} must map en/fr to nonempty strings")
        if not isinstance(entry.get("kind", ""), str):
            raise SystemExit(f"resource {identity}: kind must be a string")
        if entry.get("language", "bilingual") not in ("en", "fr", "bilingual"):
            raise SystemExit(f"resource {identity}: invalid language")
    return data


def _safe_path(raw_path: str) -> Path | None:
    """Return an existing regular file resolved inside ROOT, or None."""
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    rel = Path(raw_path)
    if rel.is_absolute() or ".." in rel.parts or "\\" in raw_path:
        return None
    try:
        resolved = (ROOT / rel).resolve(strict=True)
        resolved.relative_to(ROOT.resolve())
        return resolved if resolved.is_file() else None
    except (OSError, ValueError, RuntimeError):
        return None


def resources(language: str = "en") -> list[dict]:
    """Resolve available resources, preserving the actual source language."""
    if language not in ("en", "fr"):
        language = "en"
    result = []
    for entry in _load_raw()["resources"]:
        paths = entry["paths"]
        path_language = language if language in paths else "en"
        raw_path = paths.get(path_language)
        if raw_path is None:
            continue
        resolved = _safe_path(raw_path)
        if resolved is None:
            continue
        title_map = entry["title"]
        source_language = entry.get("language", "bilingual")
        result.append({"id": entry["id"], "kind": entry.get("kind", ""),
                       "language": entry.get("language", language),
                       "source_language": path_language if source_language == "bilingual" else source_language,
                       "title": title_map.get(language) or title_map.get("en") or entry["id"],
                       "path": resolved})
    return result


def _open_resource(resource_id: str, language: str) -> int:
    """Open only an explicitly requested, contained regular resource; no shell."""
    def fail(english, french):
        print(french if language == "fr" else english, file=sys.stderr)
        return 1
    try:
        match = next((r for r in resources(language) if r["id"] == resource_id), None)
        if match is None:
            return fail(f"resource unavailable: {resource_id}", f"ressource indisponible : {resource_id}")
        path = match["path"].resolve(strict=True)
        path.relative_to(ROOT.resolve())
        if not path.is_file():
            return fail("resource must be a regular file", "la ressource doit être un fichier ordinaire")
        if sys.platform == "win32":
            startfile = getattr(os, "startfile", None)
            if startfile is None:
                return fail("Windows file opener unavailable", "ouverture de fichiers Windows indisponible")
            startfile(str(path))
            return 0
        if sys.platform == "darwin":
            opener = "open"
        elif sys.platform.startswith("linux"):
            opener = "xdg-open"
        else:
            return fail("unsupported platform for opening resources", "plateforme non prise en charge pour ouvrir une ressource")
        result = subprocess.run([opener, str(path)], check=False)
        if result.returncode != 0:
            fail(f"resource opener failed (exit {result.returncode})", f"échec de l’ouverture (code {result.returncode})")
        return result.returncode if result.returncode >= 0 else 1
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError) as exc:
        return fail(f"cannot open resource: {exc}", f"impossible d’ouvrir la ressource : {exc}")


def _format_text(res_list: list[dict], language: str = "en") -> str:
    lines: list[str] = []
    label = "langue du contenu" if language == "fr" else "content language"
    for resource in res_list:
        lines.append(f"{resource['id']}  [{resource['kind']}]  {resource['title']}")
        lines.append(f"    {resource['path']}")
        lines.append(f"    {label}: {resource['source_language']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Factor learning resources")
    parser.add_argument("--language", choices=["en", "fr"], default=None, help="language override")
    parser.add_argument("--company", type=Path, default=None, help="company dir for preference lookup")
    parser.add_argument("--json", action="store_true", help="print as JSON")
    parser.add_argument("--open", dest="open_id", metavar="ID", help="open a resource by ID")
    args = parser.parse_args(argv[1:])

    # Resolve language: explicit flag > company pref > default en
    if args.language:
        lang = args.language
    elif args.company is not None:
        # Import here to keep this module independently usable
        _scripts = Path(__file__).parent
        sys.path.insert(0, str(_scripts))
        from preferences import load_language
        lang = load_language(args.company)
    else:
        lang = "en"

    if args.open_id:
        return _open_resource(args.open_id, lang)

    res_list = resources(lang)

    if args.json:
        printable = [
            {
                "id": r["id"],
                "kind": r["kind"],
                "language": r["language"],
                "source_language": r["source_language"],
                "title": r["title"],
                "path": str(r["path"]),
            }
            for r in res_list
        ]
        print(json.dumps(printable, indent=2, ensure_ascii=False))
    else:
        print(_format_text(res_list, lang))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
