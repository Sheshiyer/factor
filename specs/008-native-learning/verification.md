# Local verification — 2026-09-27

Status: local intake implementation and native-learning design complete. Native company/profile pilot pending; no runtime learning improvement is claimed.

## Executed checks

- `python3 -m unittest discover -s tests -v`: **237 tests passed**, including 15 bookmark intake tests. Existing 222 tests remain passing.
- Full 456-record FT JSONL cache: dry-run, explicit apply to a disposable company, repeat apply. Seven posts, twelve sources, five missing linked bodies, zero claims. Repeat receipt equal and knowledge store byte-identical. Cache unchanged. Temporary company removed after verification.
- [ingest-receipt.json](ingest-receipt.json) records cache hash, exact seven IDs, batch identity, missing X article URLs and concrete check results. Acquisition chronology remains unknown because bookmark timestamps are absent.
- Source manifest IDs and all seven post hashes match the current read-only cache. All 44 repository candidates remain disabled. All 45 shortlinks have destination receipts; resolution is not code review. Primary review and identity-only inventory are distinct.
- Intake regression checks cover cached body attribution, ambiguous article refusal, existing complete body preservation, malformed input, duplicate IDs, Unicode separators, immutable revision conflicts, traversal/symlinks, rollback and nonexecution of source instructions.
- Native source audit pins installed Hermes 0.21.5 and official upstream. No private session/memory contents or effective Factor profile configuration were inspected. Commands and settings are source-verified; real pending writes and held-out replay remain future evidence.
- New learning handoff stays in `prompts/`; no profile-loaded skill, provider, connector or schedule is enabled. Background review is proposed disabled for the first attributable manual pilot, then considered after acceptance.
- Synthesis saved through `ft library create` and read back through `ft library show`; content SHA-256: `d476e4573edccdb65d141b4ca5ea3a90681f3d6e604ecc4107f1ebd59a63cbde`.
- Local documentation links and `git diff --check` pass.

## Acceptance mapping

ISC-41: sources.json + full-cache receipt. ISC-42: seven-row synthesis and capability dispositions. ISC-43: pinned native source audit. ISC-44: intake behavior/tests. ISC-45: native operating guide and reviewed-workflow prompt. ISC-46: plan use cases, comparison metrics and rollback. ISC-47: complete suite and real-cache repeat receipt.

## Remaining evidence

Two X article bodies were unavailable: 2099316575006240776 and 2103652547227750400. Primary Company Brain repository review supplements the second without substituting for article ingestion. Embedded quote pointers and text shortlinks are not automatically expanded by the offline intake; this research expanded 45 separately.

The real native pilot needs the exact company folder and Hermes profile. Required proof: effective write gates, a successful baseline, persisted pending write without premature target mutation, founder diff review, verified approved bytes, fresh-session skill reuse and held-out evaluation. Native approvals have fail-open/config and operation-replay limitations documented in the guide. No source audit or local deterministic content trial is substituted for this runtime proof.

No push, PR, merge or deployment is included. Original checkout WIP remains preserved.
