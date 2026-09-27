#!/usr/bin/env python3
"""Review or capture a bounded Field Theory JSONL cache selection, offline."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit

import knowledge

MAX_CACHE_BYTES = 64 * 1024 * 1024


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def string(value, field, nullable=False):
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def url(value):
    value = string(value, "url")
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("url must be an HTTP(S) pointer without credentials")
    return value


def post(row):
    if not isinstance(row, dict):
        raise ValueError("selected row must be an object")
    identity = string(row.get("id"), "id")
    if not re.fullmatch(r"[0-9]+", identity):
        raise ValueError("post id must be numeric")
    if row.get("tweetId", identity) != identity:
        raise ValueError("tweetId must match id")
    if row.get("type", "post") not in {"post", "tweet", "bookmark"}:
        raise ValueError("unsupported selected row type")
    permalink = url(row.get("url"))
    parsed = urlsplit(permalink)
    if parsed.hostname not in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"} or not re.fullmatch(r"/[^/]+/status/" + identity, parsed.path):
        raise ValueError("permalink must identify the selected X post")
    text = string(row.get("text"), "text")
    author = string(row.get("authorHandle"), "authorHandle")
    published = string(row.get("postedAt"), "postedAt", nullable=True)
    bookmarked = string(row.get("bookmarkedAt"), "bookmarkedAt", nullable=True)
    links = row.get("links", [])
    if not isinstance(links, list) or len(links) > 100:
        raise ValueError("links must be a list of at most 100 URL pointers")
    links = list(dict.fromkeys(url(link) for link in links))
    quoted = row.get("quotedTweet")
    quoted_pointer = None
    if quoted is not None:
        if not isinstance(quoted, dict):
            raise ValueError("quotedTweet must be an object")
        qid = string(quoted.get("id"), "quoted id")
        if row.get("quotedStatusId", qid) != qid or not re.fullmatch(r"[0-9]+", qid):
            raise ValueError("invalid quoted identity")
        qtext = quoted.get("text")
        if qtext is not None and not isinstance(qtext, str):
            raise ValueError("quoted text must be a string")
        quoted_pointer = {"id": qid, "url": url(quoted.get("url")),
                          "body_sha256": None if qtext is None else sha(qtext.encode("utf-8")),
                          "availability": "cached_quote" if qtext is not None else "pointer_only",
                          "imported": False}
    elif row.get("quotedStatusId") is not None:
        qid = string(row["quotedStatusId"], "quotedStatusId")
        if not qid.isdecimal():
            raise ValueError("invalid quoted identity")
        quoted_pointer = {"id": qid, "url": None, "body_sha256": None,
                          "availability": "pointer_only", "imported": False}
    record = {"id": "ft:post:" + identity, "url": permalink, "author": author,
              "published_at": published, "body": text, "completeness": "complete"}
    summary = {"id": identity, "source_id": record["id"], "url": permalink,
               "author": author, "postedAt": published, "bookmarkedAt": bookmarked,
               "body_sha256": sha(text.encode("utf-8")), "status": "captured",
               "candidate_status": "needs_human_review", "quoted": quoted_pointer,
               "linked_sources": []}
    article_text = row.get("articleText")
    if article_text is not None and not isinstance(article_text, str):
        raise ValueError("articleText must be a string or null")
    article_title = row.get("articleTitle")
    if article_title is not None and not isinstance(article_title, str):
        raise ValueError("articleTitle must be a string or null")
    article_text = article_text if article_text and article_text.strip() else None
    article_links = [pointer for pointer in links
                     if re.fullmatch(r"/i/article/\d+", urlsplit(pointer).path)
                     and urlsplit(pointer).hostname in {"x.com", "twitter.com"}]
    article_link = (article_links[0] if len(article_links) == 1
                    else links[0] if len(links) == 1 else None) if article_text else None
    summary["article"] = {"title": article_title,
        "availability": "cached_bound" if article_link else "cached_unbound_needs_mapping" if article_text else "missing_body",
        "url": article_link, "body_sha256": sha(article_text.encode("utf-8")) if article_text else None}
    linked = []
    for pointer in links:
        linked_id = "ft:linked:" + sha(pointer.encode("utf-8"))
        linked_body = article_text if pointer == article_link else None
        linked.append({"id": linked_id, "url": pointer, "author": "", "published_at": None,
                       "body": linked_body, "completeness": "complete" if linked_body is not None else "missing"})
        summary["linked_sources"].append({"source_id": linked_id, "url": pointer,
            "kind": "x_article" if re.fullmatch(r"/i/article/\d+", urlsplit(pointer).path) and urlsplit(pointer).hostname in {"x.com", "twitter.com"} else "linked_page",
            "availability": "cached_body" if linked_body is not None else "missing_body",
            "body_sha256": sha(linked_body.encode("utf-8")) if linked_body is not None else None, "status": "captured"})
    return summary, [record] + linked


def prepare(cache: Path, limit=7):
    if type(limit) is not int or not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")
    cache = Path(cache)
    if not cache.is_file() or cache.is_symlink():
        raise ValueError("cache must be an explicit regular JSONL file, not a symlink")
    with cache.open("rb") as stream:
        raw = stream.read(MAX_CACHE_BYTES + 1)
    if len(raw) > MAX_CACHE_BYTES:
        raise ValueError("cache exceeds 64 MiB bound")
    selection, records, seen = [], {}, set()
    # Only LF delimits JSONL. Unicode U+2028/U+2029 are valid post characters.
    for line_number, line in enumerate(raw.decode("utf-8").split("\n"), 1):
        if not line.strip():
            continue
        if len(selection) == limit:
            break
        try:
            row = json.loads(line, object_pairs_hook=knowledge._unique_object)
            summary, sources = post(row)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"invalid selected cache row {line_number}: {exc}") from exc
        if summary["id"] in seen:
            raise ValueError(f"duplicate selected post id: {summary['id']}")
        seen.add(summary["id"])
        summary["cache_line"] = line_number
        selection.append(summary)
        for source in sources:
            previous = records.setdefault(source["id"], source)
            if previous != source:
                if previous["body"] is None and source["body"] is not None:
                    records[source["id"]] = source
                elif previous["body"] is not None and source["body"] is None:
                    pass
                else:
                    raise ValueError("conflicting source records within selected batch")
    if not selection:
        raise ValueError("cache selection is empty")
    cache_sha = sha(raw)
    batch_id = sha(canonical({"schema": 1, "cache_sha256": cache_sha,
                             "limit": limit, "ids": [item["id"] for item in selection]}))
    manifest = {"schema": "factor.bookmark-intake.v1", "batch_id": batch_id,
                "cache": str(cache.resolve()), "cache_sha256": cache_sha,
                "requested_limit": limit, "selected_count": len(selection),
                "ordering": "cache_order; newest acquisition is not proven",
                "bookmark_time_order_verified": False,
                "selection": selection, "source_count": len(records),
                "source_gaps": [item["id"] for item in records.values() if item["body"] is None],
                "link_scope": "links[] plus quoted pointer only; URLs inside text are not extracted or expanded offline",
                "unbound_articles": [item["id"] for item in selection if item["article"]["availability"] == "cached_unbound_needs_mapping"],
                "claims_created": 0, "accepted_claims_created": 0,
                "external_actions": [], "skills_installed": [], "connectors_enabled": [],
                "next_step": "Human review packet; native /learn handoff requires a separate explicit decision."}
    return manifest, list(records.values())


def write_atomic(target: Path, data: bytes):
    fd, name = tempfile.mkstemp(prefix=".bookmark-", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def ingest(cache: Path, limit=7, company: Path | None = None, apply=False, output=None):
    manifest, records = prepare(cache, limit)
    if apply and company is None:
        raise ValueError("--apply requires --company")
    if output is not None and company is None:
        raise ValueError("--output requires --company")
    root = knowledge._root(company) if company is not None else None
    target = None
    if root is not None:
        relative = output or f"wiki/intake/bookmarks-{manifest['batch_id']}.json"
        target = knowledge._safe_child(root, relative)
        if not target.is_relative_to(root / "wiki/intake") or target == root / "wiki/intake":
            raise ValueError("output must be beneath company wiki/intake/")
        manifest["company_root"] = str(root)
        manifest["receipt_path"] = str(target)
    manifest["mode"] = "applied" if apply else "dry_run"
    if not apply:
        return manifest
    # Preflight all records before any write, including immutable metadata conflicts.
    store_path = knowledge._knowledge_path(root)
    if store_path.exists() and store_path.stat().st_size > MAX_CACHE_BYTES:
        raise ValueError("existing knowledge store exceeds 64 MiB rollback bound")
    existing = knowledge._load_store(root)
    for record in records:
        normalized = knowledge._source(record)
        previous = existing["sources"].get(record["id"], {}).get("revisions", {}).get(normalized["revision"])
        if previous is not None and previous != normalized:
            raise ValueError("existing source revision has conflicting metadata")
    manifest["source_gaps_scope"] = "selected cache links only; existing company bodies are not downgraded"
    manifest["store_source_gaps"] = [record["id"] for record in records
        if record["body"] is None and existing["sources"].get(record["id"], {}).get("body") is None]
    data = canonical(manifest) + b"\n"
    if target.exists() and target.read_bytes() != data:
        raise ValueError("existing receipt differs; refusing overwrite")
    store_path = knowledge._knowledge_path(root)
    original = store_path.read_bytes() if store_path.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        for record in records:
            prior = existing["sources"].get(record["id"])
            # A cache gap must not replace a body already captured in this company.
            if record["body"] is None and prior is not None and prior["body"] is not None:
                continue
            knowledge.import_source(root, record)
        if not target.exists():
            write_atomic(target, data)
    except Exception:
        # Single-writer rollback restores exactly the prior knowledge bytes.
        if original is None:
            store_path.unlink(missing_ok=True)
        else:
            write_atomic(store_path, original)
        raise
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=7)
    parser.add_argument("--company", type=Path)
    parser.add_argument("--output", help="relative receipt path beneath wiki/intake/")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = ingest(args.cache, args.limit, args.company, args.apply, args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f"bookmark intake: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
