#!/usr/bin/env python3
"""Read and write the language preference in company/preferences.json.

API
---
    load_language(company)  -> "en" | "fr"
    save_language(company, language) -> None

CLI
---
    python3 scripts/preferences.py --company PATH
    python3 scripts/preferences.py --company PATH --set en
    python3 scripts/preferences.py --company PATH --set fr
    python3 scripts/preferences.py --company PATH --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

VALID_LANGUAGES = ("en", "fr")
DEFAULT_LANGUAGE = "en"
PREFS_FILENAME = "preferences.json"


def _prefs_path(company: Path) -> Path:
    return company / PREFS_FILENAME


def _read_preferences(company: Path) -> dict:
    path = _prefs_path(company)
    if path.is_symlink():
        raise SystemExit("preferences.json must not be a symlink")
    if not path.exists():
        return {}
    if not path.is_file():
        raise SystemExit("preferences.json must be a regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise SystemExit(f"cannot read preferences.json; preserving existing file: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("preferences.json must contain a JSON object")
    lang = data.get("language", DEFAULT_LANGUAGE)
    if lang not in VALID_LANGUAGES:
        raise SystemExit(f"preferences.json contains invalid language {lang!r}; expected en or fr")
    return data


def load_language(company: Path | None) -> str:
    """Return the preference or English when absent; reject invalid existing data."""
    if company is None:
        return DEFAULT_LANGUAGE
    return _read_preferences(Path(company)).get("language", DEFAULT_LANGUAGE)


def save_language(company: Path, language: str) -> None:
    """Atomically update a valid preference file, preserving unrelated keys.

    Symlinks (including dangling or in-company targets) and invalid existing
    preferences are rejected without repair. A single trusted writer is assumed.
    """
    if language not in VALID_LANGUAGES:
        raise SystemExit(f"invalid language {language!r}; expected en or fr")
    company = Path(company)
    if not company.is_dir():
        raise SystemExit(f"company directory does not exist: {company}")
    path = _prefs_path(company)
    existing = _read_preferences(company)
    existing["language"] = language
    temporary = None
    try:
        fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".prefs-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(existing, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        if path.is_symlink():
            raise SystemExit("preferences.json must not be a symlink")
        os.replace(temporary, path)
    except OSError as exc:
        raise SystemExit(f"cannot save preferences.json; preserving existing file: {exc}") from exc
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            except OSError:
                pass


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Read or write the language preference for a Factor company."
    )
    parser.add_argument("--company", type=Path, required=True, help="path to the company directory")
    parser.add_argument(
        "--set",
        dest="set_lang",
        choices=list(VALID_LANGUAGES),
        metavar="LANG",
        help="set the language (en or fr) and exit",
    )
    parser.add_argument("--json", action="store_true", help="print result as JSON")
    args = parser.parse_args(argv[1:])

    if args.set_lang:
        save_language(args.company, args.set_lang)
        if args.json:
            print(json.dumps({"language": args.set_lang}))
        else:
            print(args.set_lang)
        return 0

    lang = load_language(args.company)
    if args.json:
        print(json.dumps({"language": lang}))
    else:
        print(lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
