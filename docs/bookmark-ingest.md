# Capture a bounded Field Theory bookmark batch

`ingest_bookmarks.py` reads an explicitly selected local Field Theory JSONL file. It never runs `ft sync`, requests a network resource, invokes a provider, installs a skill, or enables a connector. Source text is stored as data and cannot execute commands.

Review the first seven cached records without changing files:

```sh
python3 scripts/ingest_bookmarks.py --cache /absolute/path/to/bookmarks.jsonl
```

Use `--limit 5` for five records; the supported range is 1–50 and the default is 7. Blank lines are skipped. Selected records must be valid post objects with matching numeric IDs and X permalinks, string text and author handles, optional string/null dates, and URL link lists. Field Theory's usual rows omit `type`; those rows are treated as posts. An explicit incompatible type is rejected. Duplicate selected IDs, invalid selected rows or an empty selection fail before writes. Rows after the selected limit are not validated. Cache files are bounded to 64 MiB and remain unchanged.

Selection preserves the existing cache order. It does **not** claim that this is the newest bookmark order or verified acquisition order. A missing `bookmarkedAt` stays `null`; a post date is not substituted for bookmark time. JSONL is split only on LF, preserving Unicode U+2028/U+2029 inside post bodies.

The default stdout manifest contains source pointers, authors, posting/bookmark dates, post body SHA-256 values, quoted-post pointers, missing linked-page bodies, cache SHA-256, selected line numbers and a stable batch ID. It contains no post or quoted bodies. Every candidate requires human review. This command does not extract or accept claims.

## Apply to an explicitly selected company

The company root must already exist. First inspect its proposed manifest:

```sh
python3 scripts/ingest_bookmarks.py --cache /absolute/path/to/bookmarks.jsonl \
  --company /absolute/path/to/company --limit 7
```

Then capture the batch locally:

```sh
python3 scripts/ingest_bookmarks.py --cache /absolute/path/to/bookmarks.jsonl \
  --company /absolute/path/to/company --limit 7 --apply
```

Apply requires `--company`. It imports selected post bodies through `knowledge.import_source`, preserving their exact text in `wiki/knowledge.json`. Post source IDs are `ft:post:<id>`; linked sources use a SHA-256 of their URL. Sources have intake status `captured` in the receipt. No new claims are created, and no existing claim is automatically accepted.

A linked article or repository URL is a pointer, not its body. When `articleText` is present, the importer captures it only when it can bind it to exactly one X article link or a sole link. With multiple ambiguous targets, it retains an article hash/title and `cached_unbound_needs_mapping` status without assigning the text to an arbitrary URL. Invalid article text/title types are rejected. Each distinct link without a bound cached article body becomes a separate source with `body: null` and `completeness: missing`, unless the company already has a captured body for that linked source. A cache gap never downgrades an existing body; receipt gaps describe the cache evidence. X article pointers are labeled `x_article`; other links are labeled `linked_page`. Gap counts cover `links[]` only; URLs embedded in post or quote text are not extracted or expanded. Applied receipts distinguish cache gaps from remaining company-store gaps. Embedded quote text is not imported in this pass: its pointer and body hash appear for later review. Source-level `complete` means the cached selected post text was captured, not that its claims, thread, quotes, article, or referenced resources were verified.

The immutable receipt defaults to `wiki/intake/bookmarks-<batch-id>.json`. To choose a name, use a company-relative path beneath `wiki/intake/`:

```sh
python3 scripts/ingest_bookmarks.py --cache /absolute/path/to/bookmarks.jsonl \
  --company /absolute/path/to/company --output wiki/intake/review-batch.json --apply
```

A repeat with identical cache, selection, paths and company reuses the receipt and source revisions without rewriting them. An altered receipt or a conflicting existing immutable source revision is rejected. A changed cache or different limit produces a different batch identity. A custom fixed receipt filename therefore rejects a different batch instead of replacing prior evidence.

Traversal and company/output symlinks are rejected through the existing knowledge path guards. The importer preflights all immutable source metadata before importing and rejects an existing knowledge store larger than 64 MiB to bound rollback memory. If a later import or receipt write fails, it restores the knowledge file's exact previous bytes (or removes the newly created knowledge file). Empty intake directories can remain. This is a **single-writer, trusted-local-operator** operation; rollback is not safe against another simultaneous writer, and the path checks are not a hostile multi-user filesystem sandbox.

## Review and native learning handoff

Read the receipt first, then inspect the selected source versions in the company knowledge store. Distinguish directly captured post text, quoted pointers and missing linked content. The next action is a human review packet and an explicitly chosen native `/learn` handoff in the appropriate runtime. This script does not run `/learn`, assume that Factor's Hermes profile is installed, or invent a headless native-learning command. Review and accept claims separately using the [knowledge-curation workflow](knowledge-curation.md).

Test the bounded intake locally:

```sh
python3 -m unittest discover -s tests -p test_ingest_bookmarks.py -v
```
