# Sync and ingestion receipt

Date: 2026-09-27. Field Theory CLI: `1.3.22`.

## Fresh sync

Command: `ft sync --no-media --max-minutes 5`.

Result: exit **1**, before a successful refresh. Error: `No ct0 CSRF cookie found for x.com in Google Chrome.` The CLI reported the Default profile. No cookies, tokens or credential files were copied into this packet. No alternate browser/profile was guessed.

Pre-sync status: 444 cached bookmarks, all 444 classified; cache last updated `2026-09-25T12:56:26.091Z`. `connected: false` describes the reported connection status and is not by itself a check of every possible browser session.

Resume: identify the already-authenticated supported browser/profile, rerun `ft sync --no-media` with that selector, verify status, then re-scan the full cache and reconcile by source ID/hash. Use `ft sync --help` for current flags. Never paste authentication tokens into a research note or chat. Gap backfill is a separate retrieval step; a successful incremental sync alone does not prove every linked article body is present.

## External refresh observed

At verification, the cache had changed to **456 records**, all classified, with `lastUpdated: 2026-09-27T10:09:33.364Z`. The writer was not identified. The initial `ft sync` invocation still exited 1; this later state must not be reported as its success. The complete scan and manifest were regenerated, adding five candidates (four curated and one shelved).

## Cached ingestion

Read-only corpus: `/Users/sheshnarayaniyer/.fieldtheory/bookmarks/bookmarks.db`. Reading copies: `/Users/sheshnarayaniyer/.fieldtheory/library/bookmarks/`.

Final pass scanned all 456 rows, matching case-insensitive `hermes`, whole-word `jev`, `grok.?bot`, `grok agents`, `knowledge`, `curation`, `compaction`, `correction`, or `memory` across text, article title/body and quoted tweet. Broad matching intentionally catches incidental mentions; curation dispositions prevent them becoming accepted guidance.

Output: 92 candidates, 22 cached article bodies; 36 curated, 44 shelf, 12 excluded. Full post/article bodies remain in the source store. `sources.json` retains SHA-256 for post text and, when present, article text, plus timestamps and source locators. There is no date filter or result-limit cutoff in this full-cache scan.

## Known linked-article gaps

| Cached record | Missing or unresolved source |
|---|---|
| `2100672929533137107` | Quoted guide `https://x.com/everestchris6/status/2100668987956937158` |
| `2099284683012121073` | Quoted guide `https://x.com/everestchris6/status/2099161324555309092` |
| `2102453475078533209` | Quoted source `https://x.com/maestrooth/status/2092658066714177657` |
| `2087897918733000904` | Quoted source `https://x.com/VibeMarketer_/status/2087894971257110685` |
| `2103195240924598623` | Quoted source `https://x.com/Argona0x/status/2091898304900571501` |

These pointers are follow-up leads, not proof of having read their bodies. Other post-only records may be complete standalone posts; absence of an article body does not automatically mean truncation.

The newly observed Company Brain author post (`2103668051468300701`) links `https://x.com/i/article/2103652547227750400`. Its full body was not cached and web retrieval failed; the public project README was checked separately.

## Review limitations

A routed `noesis-observe` read-only review returned content, but its receipt reported `UNRESOLVED` with missing session attribution. It cannot be credited to a verified provider/model. Several findings were refuted by direct source inspection: onboarding does create wiki, instinct, profile soul and eval/I/O files, and the intent writer does validate room and door values. Those incorrect findings were excluded from the implementation brief.

The separate advisor CLI exited with a usage-credit error for its configured 1M context. No billing setting or model configuration was changed. Final evidence rests on direct corpus and repository inspection.

The optional local phase console at `127.0.0.1:5173` refused its browser connection. This does not establish anything about the separately reported Manifest bridge or Hermes runtime.
