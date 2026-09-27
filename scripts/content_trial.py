#!/usr/bin/env python3
"""Assemble a local review packet from reviewed evidence and supplied prose."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import knowledge
import corrections


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("expected a relative path without traversal")
    candidate = root
    for part in rel.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError(f"symlink not allowed: {relative}")
    candidate.resolve().relative_to(root.resolve())
    return candidate


# Citation markup is opaque to prose corrections. Also protect code, reference
# definitions, footnotes and bare URLs. This is deliberately not a Markdown renderer.
PROTECTED = re.compile(
    r"```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`|"
    r"^ {0,3}\[[^\]\n]+\]:[^\n]*(?:\n[ \t]+[^\n]*)*|"
    r"!?\[\[[^\]\n]+\]\]|!?\[[^\]\n]*\]\([^\n]*\)|"
    r"!?\[[^\]\n]*\]\[[^\]\n]*\]|\[[^\]\n]+\]|"
    r"<https?://[^>\n]+>|https?://[^\s<>]+", re.MULTILINE)


def protected_ranges(text: str):
    ranges = [(m.start(), m.end()) for m in PROTECTED.finditer(text)]

    def balanced(start, opening, closing):
        depth, index = 0, start
        while index < len(text):
            char = text[index]
            if char == "\\":
                index += 2
                continue
            if char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return index + 1
            index += 1
        return len(text)  # Incomplete markup is conservatively opaque.

    cursor = 0
    while cursor < len(text):
        start = text.find("[", cursor)
        if start < 0:
            break
        end = balanced(start, "[", "]")
        if end < len(text) and text[end] in "([":
            opening = text[end]
            end = balanced(end, opening, ")" if opening == "(" else "]")
        ranges.append((start, end))
        cursor = end
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def corrected_prose(root: Path, page: str, text: str) -> str:
    pieces, cursor = [], 0
    for start, end in protected_ranges(text):
        pieces.append(corrections.apply_corrections(root, page, text[cursor:start]))
        pieces.append(text[start:end])
        cursor = end
    pieces.append(corrections.apply_corrections(root, page, text[cursor:]))
    return "".join(pieces)


def run_trial(root: Path, page: str, draft: str, card_id: str,
              output_dir: str = "output/content-trials") -> dict:
    root = Path(root)
    if root.is_symlink():
        raise ValueError("company root must not be a symlink")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("company root must be a directory")
    if not isinstance(draft, str) or not draft.strip():
        raise ValueError("founder supplied draft text is required")
    if not isinstance(card_id, str) or not card_id.strip():
        raise ValueError("card identity is required")
    safe_path(root, "wiki/" + page)
    wiki = safe_path(root, "wiki")
    # Dependencies read these stores. Reject symbolic links before consuming them.
    for directory, dirs, files in os.walk(wiki, followlinks=False):
        for name in dirs + files:
            if (Path(directory) / name).is_symlink():
                raise ValueError("wiki contains a symlink")
    out = safe_path(root, output_dir)
    if not out.relative_to(root).parts or out.relative_to(root).parts[0] != "output":
        raise ValueError("review packets must be beneath output/")
    evidence = knowledge.retrieve(root, page)
    claims = evidence.get("claims", [])
    blockers = []
    if not claims:
        blockers.append("no accepted claims")
    if evidence.get("gaps"):
        blockers.append("source gaps require review")
    if evidence.get("stale_revisions"):
        blockers.append("stale source revisions require review")
    if evidence.get("conflicts"):
        blockers.append("conflicting claims require review")
    for claim in claims:
        if claim.get("status") != "accepted" or not claim.get("locator"):
            blockers.append("invalid accepted claim provenance")
        if not re.fullmatch(r"[0-9a-f]{64}", str(claim.get("source_revision", ""))):
            blockers.append("invalid source revision")
        source = evidence.get("sources", {}).get(claim.get("source_id"), {})
        if claim.get("source_revision") not in source.get("revisions", {}):
            blockers.append("claim source revision evidence is missing")
    input_record = {"company_root": str(root), "card_id": card_id,
                    "page": evidence.get("page", page), "founder_draft": draft,
                    "retrieval": evidence}
    corrected = None if blockers else corrected_prose(root, evidence["page"], draft)
    packet = {"schema": "factor.content-trial.v1", "company_root": str(root),
              "card_id": card_id, "page": evidence.get("page", page),
              "status": "blocked" if blockers else "local_review_required",
              "local_only": True, "published": False, "external_actions": [],
              "draft_origin": "founder_supplied", "blockers": sorted(set(blockers)),
              "draft": corrected, "claims": claims,
              "source_versions": evidence.get("sources", {}),
              "gaps": evidence.get("gaps", []), "conflicts": evidence.get("conflicts", []),
              "stale_revisions": evidence.get("stale_revisions", []),
              "citation_policy": "Evidence is attached for review; prose entailment and existing citations are not automatically verified."}
    input_sha256 = digest(input_record)
    output_sha256 = digest(packet)
    receipt = {"input_sha256": input_sha256, "output_sha256": output_sha256,
               "packet": packet}
    data = canonical(receipt) + b"\n"
    out.mkdir(parents=True, exist_ok=True)
    target = safe_path(root, str(out.relative_to(root) / f"{input_sha256}-{output_sha256}.json"))
    deduplicated = target.exists()
    if deduplicated:
        if target.read_bytes() != data:
            raise ValueError("content-addressed packet was modified; refusing overwrite")
    else:
        fd, temporary = tempfile.mkstemp(prefix=".trial-", dir=out)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return {"path": str(target), "deduplicated": deduplicated,
            "input_sha256": input_sha256, "output_sha256": output_sha256,
            "status": packet["status"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--page", required=True)
    parser.add_argument("--card-id", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--draft-file", help="UTF-8 file relative to company root")
    parser.add_argument("--output-dir", default="output/content-trials")
    args = parser.parse_args(argv)
    try:
        if args.root.is_symlink():
            raise ValueError("company root must not be a symlink")
        text = args.text
        if args.draft_file:
            text = safe_path(args.root.resolve(strict=True), args.draft_file).read_text(encoding="utf-8")
        result = run_trial(args.root, args.page, text, args.card_id, args.output_dir)
        print(json.dumps(result, indent=2))
        return 1 if result["status"] == "blocked" else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"content trial: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
