#!/usr/bin/env python3
"""Local company source revisions, reviewed claims, and indexed retrieval.

Mutations require a single writer per company. Atomic replacement protects readers
from partial JSON; the exclusive temporary file rejects overlapping commits but
is not a transaction lock across the complete read/modify/write operation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

KNOWLEDGE_FILE = "knowledge.json"
REVIEW_STATUSES = {"captured", "extracted", "accepted", "rejected", "disputed", "superseded"}
COMPLETENESS = {"complete", "partial", "missing"}
CLAIM_FIELDS = ("id", "subject", "predicate", "statement", "source_id", "source_revision", "locator", "page")


def _text(value: Any, name: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{name} must be a {'possibly empty ' if empty else 'non-empty '}string")
    return value


def _checked(path: Path) -> Path:
    # Keep lexical components until symlinks have been rejected. /tmp itself can
    # be a platform alias; only ancestors above the supplied root are trusted.
    if path.is_symlink():
        raise ValueError(f"symlink not allowed: {path}")
    return path


def _root(root: Path) -> Path:
    root = Path(root)
    if ".." in root.parts:
        raise ValueError("root traversal not allowed")
    current = Path(root.anchor) if root.is_absolute() else Path.cwd()
    for part in root.parts[1:] if root.is_absolute() else root.parts:
        current /= part
        # macOS standard temporary-directory aliases are trusted mount roots.
        if str(current) not in {"/tmp", "/var"}:
            _checked(current)
    _checked(root)
    if not root.is_dir():
        raise ValueError("company root must be an existing directory")
    return root.resolve()


def _safe_child(root: Path, rel: str) -> Path:
    root = _root(root)
    _text(rel, "path")
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts or "\\" in rel or "\x00" in rel:
        raise ValueError(f"path escapes root: {rel!r}")
    current = root
    for part in path.parts:
        current = _checked(current / part)
    return current


def _wiki_dir(root: Path) -> Path:
    return _safe_child(root, "wiki")


def _knowledge_path(root: Path) -> Path:
    return _safe_child(root, "wiki/" + KNOWLEDGE_FILE)


def _revision_digest(record: dict[str, Any]) -> str:
    body = record.get("body")
    return "missing" if body is None else hashlib.sha256(body.encode("utf-8")).hexdigest()


def _source(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("source must be an object")
    sid = _text(record.get("id"), "source id")
    body = record.get("body")
    if body is not None:
        _text(body, "body", empty=True)
    completeness = record.get("completeness", "missing" if body is None else "complete")
    if not isinstance(completeness, str) or completeness not in COMPLETENESS:
        raise ValueError("invalid source completeness")
    if (body is None) != (completeness == "missing"):
        raise ValueError("missing completeness requires a missing body and vice versa")
    published = record.get("published_at")
    if published is not None:
        _text(published, "published_at")
    revision = _revision_digest(record)
    return {"id": sid, "url": _text(record.get("url", ""), "url", empty=True),
            "author": _text(record.get("author", ""), "author", empty=True),
            "published_at": published, "body": body, "completeness": completeness,
            "revision": revision, "content_sha256": None if body is None else revision}


def _page_name(page: Any) -> str:
    page = _text(page, "page")
    decoded = unquote(page)
    if decoded != page:
        page = decoded
    if urlsplit(page).scheme or urlsplit(page).netloc or "?" in page or "#" in page:
        raise ValueError("page must be a local wiki path")
    if Path(page).is_absolute() or ".." in Path(page).parts or "\\" in page or "\x00" in page:
        raise ValueError("page escapes wiki root")
    normalized = Path(page).as_posix()
    if normalized.startswith("wiki/"):
        normalized = normalized[5:]
    if not normalized or normalized == ".":
        raise ValueError("page must name a Markdown file")
    if not Path(normalized).suffix:
        normalized += ".md"
    if Path(normalized).suffix != ".md":
        raise ValueError("page must name a Markdown file")
    return normalized


def _claim(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("claim must be an object")
    result = {field: _text(record.get(field), f"claim {field}") for field in CLAIM_FIELDS}
    result["page"] = _page_name(result["page"])
    effective = record.get("effective_at")
    if effective is not None:
        _text(effective, "effective_at")
    result["effective_at"] = effective
    result["status"] = record.get("status", "captured")
    if not isinstance(result["status"], str) or result["status"] not in REVIEW_STATUSES:
        raise ValueError("invalid claim status")
    return result


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate knowledge record key: {key!r}")
        result[key] = value
    return result


def _load_store(root: Path) -> dict[str, Any]:
    path = _knowledge_path(root)
    if not path.exists():
        return {"sources": {}, "claims": {}}
    if not path.is_file():
        raise ValueError("knowledge store must be a regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("invalid knowledge store") from exc
    if not isinstance(data, dict) or set(data) != {"sources", "claims"}:
        raise ValueError("invalid knowledge store shape")
    if not all(isinstance(data[k], dict) for k in ("sources", "claims")):
        raise ValueError("sources and claims must be mappings")
    for sid, source in data["sources"].items():
        normalized = _source(source)
        if normalized["id"] != sid or any(source.get(k) != v for k, v in normalized.items()):
            raise ValueError("source identity or content hash mismatch")
        if set(source) - set(normalized) - {"revisions", "prior_revision"}:
            raise ValueError("unknown source record fields")
        revisions = source.get("revisions")
        if not isinstance(revisions, dict) or source["revision"] not in revisions:
            raise ValueError("source must retain its immutable revisions")
        if "prior_revision" in source and (not isinstance(source["prior_revision"], str) or source["prior_revision"] not in revisions):
            raise ValueError("invalid prior revision")
        for digest, old in revisions.items():
            normalized_old = _source(old)
            if old != normalized_old or old["id"] != sid or old["revision"] != digest:
                raise ValueError("invalid source revision or content hash")
        if revisions[source["revision"]] != normalized:
            raise ValueError("latest source differs from immutable revision")
    for cid, claim in data["claims"].items():
        if claim != _claim(claim) or cid != claim["id"]:
            raise ValueError("invalid claim record")
        source = data["sources"].get(claim["source_id"])
        if source is None:
            raise ValueError(f"claim {cid!r} references missing source")
        if claim["source_revision"] not in source["revisions"]:
            raise ValueError(f"claim {cid!r} references missing source revision")
    return data


def _atomic_write(root: Path, data: dict[str, Any]) -> None:
    wiki = _wiki_dir(root)
    wiki.mkdir(exist_ok=True)
    target = _knowledge_path(root)
    tmp = _safe_child(root, "wiki/knowledge.json.new")
    # Exclusive creation prevents following a pre-existing temporary symlink or
    # overwriting another pending transaction. Replacement is on the same volume.
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        _knowledge_path(root)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()


def import_source(root: Path, record: dict[str, Any]) -> str:
    source = _source(record)
    store = _load_store(root)
    sid, digest = source["id"], source["revision"]
    existing = store["sources"].get(sid)
    revisions = {} if existing is None else dict(existing["revisions"])
    if digest in revisions:
        if revisions[digest] != source:
            raise ValueError("same source revision has conflicting metadata")
        return digest
    revisions[digest] = source.copy()
    store["sources"][sid] = {**source, "revisions": revisions}
    if existing is not None:
        store["sources"][sid]["prior_revision"] = existing["revision"]
    _atomic_write(root, store)
    return digest


def add_claim(root: Path, claim: dict[str, Any]) -> str:
    normalized = _claim(claim)
    if normalized["status"] != "captured":
        raise ValueError("new claims must be captured; review explicitly")
    store = _load_store(root)
    source = store["sources"].get(normalized["source_id"])
    if source is None:
        raise ValueError("unknown source_id")
    if normalized["source_revision"] not in source["revisions"]:
        raise ValueError("source revision mismatch")
    # Validate path components even when the page is not authored yet.
    _safe_child(root, "wiki/" + normalized["page"])
    cid = normalized["id"]
    old = store["claims"].get(cid)
    if old is not None:
        if {**old, "status": "captured"} != normalized:
            raise ValueError("claim id already exists with conflicting content")
        return cid
    store["claims"][cid] = normalized
    _atomic_write(root, store)
    return cid


def review_claim(root: Path, claim_id: str, status: str) -> None:
    _text(claim_id, "claim_id")
    if not isinstance(status, str) or status not in REVIEW_STATUSES:
        raise ValueError("invalid status")
    store = _load_store(root)
    if claim_id not in store["claims"]:
        raise ValueError("unknown claim_id")
    store["claims"][claim_id]["status"] = status
    _atomic_write(root, store)


def _resolve_page(root: Path, page: str, *, stem: bool = False) -> str:
    normalized = _page_name(page)
    path = _safe_child(root, "wiki/" + normalized)
    if stem and "/" not in normalized:
        wiki = _wiki_dir(root)
        candidates = []
        # Never traverse symlinked directories while resolving legacy [[owner]].
        for current, dirs, files in os.walk(wiki, followlinks=False):
            for name in dirs + files:
                if (Path(current) / name).is_symlink():
                    raise ValueError("symlink not allowed in wiki")
            if normalized in files:
                candidates.append((Path(current) / normalized).relative_to(wiki).as_posix())
        if not candidates:
            raise ValueError(f"missing wiki page {page}")
        if len(candidates) != 1:
            raise ValueError(f"wiki stem must resolve uniquely: {page!r}")
        normalized = candidates[0]
        path = _safe_child(root, "wiki/" + normalized)
    if not path.is_file():
        raise ValueError(f"page not found in wiki: {page!r}")
    return normalized


def _index_targets(root: Path) -> list[tuple[str, bool]]:
    index = _safe_child(root, "wiki/index.md")
    if not index.is_file():
        raise ValueError("wiki/index.md is required")
    text = index.read_text(encoding="utf-8")
    # Comments and fenced/inline code are not navigable index links.
    text = re.sub(r"<!--.*?-->|```.*?```|~~~.*?~~~|`[^`]*`", "", text, flags=re.S)
    targets = [(m.group(1).split("|", 1)[0].strip(), True)
               for m in re.finditer(r"\[\[([^]\n]+)\]\]", text)]
    targets += [(m.group(1).strip().strip("<>"), False)
                for m in re.finditer(r"(?<!!)\[[^]\n]*\]\(([^)\n]+)\)", text)]
    return [(target.split("#", 1)[0], wiki_link) for target, wiki_link in targets
            if target.split("#", 1)[0]]


def _indexed_pages(root: Path) -> set[str]:
    return {_resolve_page(root, target, stem=wiki_link and "/" not in target)
            for target, wiki_link in _index_targets(root)}


def wiki_index_problems(root: Path) -> list[str]:
    """Checker diagnostics for every link; legacy companies may omit an index.

    Retrieval separately requires an index. Links share the exact same resolver
    as retrieval, including path boundaries and unique wiki stem resolution.
    """
    try:
        index = _safe_child(root, "wiki/index.md")
        if not index.exists():
            return []
        targets = _index_targets(root)
    except (ValueError, OSError) as exc:
        return [str(exc)]
    problems = []
    for target, wiki_link in targets:
        try:
            _resolve_page(root, target, stem=wiki_link and "/" not in target)
        except (ValueError, OSError) as exc:
            problems.append(str(exc) if str(exc) == f"missing wiki page {target}"
                            else f"invalid wiki page {target}: {exc}")
    return problems


def retrieve(root: Path, page: str) -> dict[str, Any]:
    normalized = _resolve_page(root, page, stem="/" not in page and not Path(page).suffix)
    if normalized not in _indexed_pages(root):
        raise ValueError(f"page {page!r} not indexed in wiki/index.md")
    store = _load_store(root)
    accepted = [c for c in store["claims"].values()
                if c["status"] == "accepted" and c["page"] == normalized]
    gaps, stale, evidence, groups = set(), [], {}, {}
    for claim in accepted:
        sid = claim["source_id"]
        source = store["sources"][sid]
        digest = claim["source_revision"]
        revision = source["revisions"][digest]
        if revision["completeness"] != "complete":
            gaps.add(sid)
        if digest != source["revision"]:
            stale.append({"claim_id": claim["id"], "source_id": sid,
                          "source_revision": digest, "latest_revision": source["revision"]})
        item = evidence.setdefault(sid, {"revision": source["revision"], "url": source["url"], "revisions": {}})
        item["revisions"][digest] = {key: value for key, value in revision.items() if key != "body"}
        groups.setdefault((claim["subject"], claim["predicate"]), []).append(claim)
    conflicts = [group for group in groups.values() if len({c["statement"] for c in group}) > 1]
    return {"page": normalized, "text": _safe_child(root, "wiki/" + normalized).read_text(encoding="utf-8"),
            "claims": accepted, "gaps": sorted(gaps), "conflicts": conflicts,
            "sources": evidence, "stale_revisions": stale}


def _cmd_import_source(args: argparse.Namespace) -> int:
    root = Path(args.root)
    record: dict[str, Any] = {"id": args.id}
    if args.url:
        record["url"] = args.url
    if args.author:
        record["author"] = args.author
    if args.published_at:
        record["published_at"] = args.published_at
    # body is None unless explicitly provided
    record["body"] = args.body
    if args.completeness:
        record["completeness"] = args.completeness
    try:
        digest = import_source(root, record)
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps({"id": record["id"], "revision": digest}, indent=2))
    return 0


def _cmd_add_claim(args: argparse.Namespace) -> int:
    root = Path(args.root)
    claim: dict[str, Any] = {
        "id": args.id,
        "subject": args.subject,
        "predicate": args.predicate,
        "statement": args.statement,
        "source_id": args.source_id,
        "source_revision": args.source_revision,
        "locator": args.locator,
        "page": args.page,
    }
    if args.effective_at:
        claim["effective_at"] = args.effective_at
    try:
        claim_id = add_claim(root, claim)
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps({"claim_id": claim_id}, indent=2))
    return 0


def _cmd_review(args: argparse.Namespace) -> int:
    root = Path(args.root)
    try:
        review_claim(root, args.claim_id, args.status)
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps({"claim_id": args.claim_id, "status": args.status}, indent=2))
    return 0


def _cmd_retrieve(args: argparse.Namespace) -> int:
    root = Path(args.root)
    try:
        result = retrieve(root, args.page)
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog="knowledge",
        description="Company knowledge store: sources, claims, retrieval.",
    )
    parser.add_argument("--root", default=".", help="company root directory")
    sub = parser.add_subparsers(dest="command")

    # import-source
    p_import = sub.add_parser("import-source", help="Register a source")
    p_import.add_argument("--id", required=True)
    p_import.add_argument("--url", default="")
    p_import.add_argument("--author", default="")
    p_import.add_argument("--published-at", dest="published_at", default=None)
    p_import.add_argument("--body", default=None)
    p_import.add_argument("--completeness", default=None)

    # add-claim
    p_claim = sub.add_parser("add-claim", help="Add a claim")
    p_claim.add_argument("--id", required=True)
    p_claim.add_argument("--subject", required=True)
    p_claim.add_argument("--predicate", required=True)
    p_claim.add_argument("--statement", required=True)
    p_claim.add_argument("--source-id", dest="source_id", required=True)
    p_claim.add_argument("--source-revision", dest="source_revision", required=True)
    p_claim.add_argument("--locator", required=True)
    p_claim.add_argument("--effective-at", dest="effective_at", default=None)
    p_claim.add_argument("--page", required=True)

    # review
    p_review = sub.add_parser("review", help="Set a claim review status")
    p_review.add_argument("--claim-id", dest="claim_id", required=True)
    p_review.add_argument("--status", required=True, choices=sorted(REVIEW_STATUSES))

    # retrieve
    p_retrieve = sub.add_parser("retrieve", help="Retrieve accepted claims for a page")
    p_retrieve.add_argument("--page", required=True)

    args = parser.parse_args(argv[1:])

    if args.command == "import-source":
        return _cmd_import_source(args)
    if args.command == "add-claim":
        return _cmd_add_claim(args)
    if args.command == "review":
        return _cmd_review(args)
    if args.command == "retrieve":
        return _cmd_retrieve(args)

    parser.print_help(file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
