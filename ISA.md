---
project: factor
effort: E3
phase: verify
progress: 84/86
mode: algorithm
started: 2026-09-22
updated: 2026-09-27
---

# Factor

## Problem

The bookmark catalog is real, and a profile install would still load all 60 offered cards. They lived under `skills/`, which Hermes owns. The picker did not show risk, approval, or whether a repository exists, and a written choice did not place the card in the company repo.

## Vision

Skills, plugins, and other capabilities are three doors. A person or an agent opens one, reads the cost, and takes only what this company will use. The profile keeps the operator. The company keeps the choice.

## Out of Scope

Upstream skill bodies. A live Hermes profile install. Invented repository URLs. A curses dependency. Composio as a catalog row. Enabling shelf items.

## Principles

A tool the company did not choose does not sit in the agent's prompt. The human menu and the agent menu are the same registry.

## Constraints

Hermes profile install owns `skills/` at the repo root. Catalog cards stay outside that tree until onboarding copies a chosen card into a company repo. Stdlib only.

## Goal

Release follow-up: commit the completed framework work, bump to v0.6.0 and publish a GitHub release from a CI-verified merged commit. Preserve the original checkout and distinguish release source from installed/runtime acceptance.

Current follow-up: reconcile GitHub and prior memory work, write spec 007, and execute the local knowledge/approval/correction/content loop using temperance-parallel-dispatch. Verification and scope limits: `specs/007-knowledge-curation/verification.md`. Prior research and criteria 1–32 remain historical records.

2026-09-27 research extension: curate the available Field Theory corpus into a traceable research packet and implementation brief for Factor. Attempt a fresh sync, record its real result, and keep inaccessible material explicitly pending.

A founder or an agent chooses offered skills, plugins, and other capabilities by category. The choice is written to that company's `connectors/enabled.yaml`, and only those cards are copied into that company's `skills/`.

## Criteria

- [x] ISC-81: Distribution metadata declares version 0.6.0.
- [x] ISC-82: Release notes describe features, upgrade path and unresolved runtime checks.
- [x] ISC-83: Release source passes Python tests, Swift tests/build and media hash verification.
- [ ] ISC-84: GitHub main contains the release commit after successful pull-request CI.
- [ ] ISC-85: Published v0.6.0 tag resolves to the merged release commit.
- [x] ISC-86: Anti: original checkout research and ISA edits remain preserved.

- [x] ISC-1: `skills/catalog/` does not exist.
- [x] ISC-2: `catalog/cards/openspec/SKILL.md` exists and names `Fission-AI/OpenSpec`.
- [x] ISC-3: `catalog/cards/` contains one directory per registry row with disposition `add`.
- [x] ISC-4: `skills/catalog-onboard/SKILL.md` exists and names `scripts/onboard.py`.
- [x] ISC-5: `distribution.yaml` owns `skills` and does not own `catalog`.
- [x] ISC-6: `--json --category skills` exits 0 and every row has category skills.
- [x] ISC-7: That output includes `openspec` and excludes `refactoring-ui`.
- [x] ISC-8: `--json --category plugins` includes `refactoring-ui` and `pixelrag`.
- [x] ISC-9: `--json --category other` includes `tinyfish` and `firecrawl`.
- [x] ISC-10: `--json` contains no id `composio`.
- [x] ISC-11: `--text --category skills` prints `SKILLS` and does not print `PLUGINS`.
- [x] ISC-12: `--enable goose` exits non-zero and mentions shelf.
- [x] ISC-13: `--enable not-a-tool` exits non-zero and mentions unknown.
- [x] ISC-14: `--company` plus `--enable openspec` writes `enabled.yaml` and copies `skills/openspec/SKILL.md`.
- [x] ISC-15: That copied card contains the OpenSpec repository URL.
- [x] ISC-16: `--enable-category plugins` writes `refactoring-ui` and `pixelrag` and no skill id.
- [x] ISC-17: `check_company.py` reports a missing card when `openspec` is enabled without `skills/openspec/SKILL.md`.
- [x] ISC-18: A company with the copied card does not fail the connector check for that id.
- [x] ISC-19: Anti: `sync_catalog.py` does not recreate `skills/catalog/`.
- [x] ISC-20: Anti: a non-tty run with no flags exits 0 without reading stdin.
- [x] ISC-21: This file contains `## Goal` and `## Criteria`.

- [x] ISC-22: A sync receipt records the actual ft sync exit result.
- [x] ISC-23: The research manifest records the full cache record count.
- [x] ISC-24: Every candidate has a stable source ID and URL.
- [x] ISC-25: Each cached article body has a SHA-256 in the manifest.
- [x] ISC-26: Every candidate has a recorded curation disposition.
- [x] ISC-27: The synthesis maps the hand and glove to existing Factor files.
- [x] ISC-28: The synthesis distinguishes authority from decision confidence.
- [x] ISC-29: The implementation brief specifies a provenance-preserving knowledge lifecycle.
- [x] ISC-30: The brief names observable acceptance checks for each proposed change.
- [x] ISC-31: Missing linked article bodies are recorded as gaps.
- [x] ISC-32: Anti: research ingestion enables no new connector or profile skill.

## Knowledge implementation extension

- [x] ISC-33: GitHub history and current phase reconcile without reopening completed work.
- [x] ISC-34: Source imports are revisioned and idempotent; missing content remains explicit.
- [x] ISC-35: Indexed retrieval rejects escaped paths and surfaces provenance and conflicts.
- [x] ISC-36: Exact-action human approval is required regardless of confidence.
- [x] ISC-37: Reviewed correction affects next local draft and rejects stale or conflicting acceptance.
- [x] ISC-38: Shadow Jev results validate candidates and receipts without claiming live calls.
- [x] ISC-39: Failed compaction preserves context and retained messages remain byte-identical.
- [x] ISC-40: Content trial deduplicates, preserves citations, and passes the complete local suite.

## Latest-seven native learning extension

- [x] ISC-41: Selected seven source IDs and cache-order uncertainty are preserved with hashes.
- [x] ISC-42: Each bookmark has a sourced use-case and adopt/adapt/defer or gap decision.
- [x] ISC-43: Installed and upstream Hermes learning mechanisms are distinguished with source evidence.
- [x] ISC-44: Repeatable bookmark intake stages sources without accepting claims or installing skills.
- [x] ISC-45: Native learning handoff specifies reviewed memory/skill writes and next-session replay evidence.
- [x] ISC-46: Integration plan names a usable pilot, success metrics and promotion/rollback boundaries.
- [x] ISC-47: Intake dry-run, repeat ingestion and full local suite are verified.

## Test Strategy

Release probes: read distribution.yaml and release notes (ISC-81–82); execute Python/Swift checks and SHA-256 validation (ISC-83); inspect GitHub PR checks and main ref (ISC-84); compare published tag/ref (ISC-85); compare original working-file hashes (ISC-86).

Research extension: compare manifest IDs, hashes and count against the read-only cache; inspect synthesis and brief; run git diff boundary checks. Historical ISC-1–21 remain prior evidence, not fresh runtime acceptance.

| ISC | Type | Check | Tool |
|---|---|---|---|
| 1–5, 19, 21 | file | path exists or is absent, and a string match | `rg` or unittest |
| 6–13, 20 | cli | onboard stdout and exit code, stdin not a tty | `python3 -m unittest` |
| 14–18 | cli | temp company, then onboard and check_company | `python3 -m unittest` |

## Features

Release v0.6.0: metadata and notes (ISC-81–82), local verification (ISC-83), PR/CI/merge and tag publication (ISC-84–85), original work preservation (ISC-86). These steps form a sequential release chain.

Research extension: sync receipt (ISC-22); source inventory (ISC-23–26, ISC-31); architecture synthesis (ISC-27–28); implementation brief (ISC-29–30); boundary verification (ISC-32). These are documentation artifacts, not runtime activation.

| Name | Satisfies | Depends on | Parallelizable |
|---|---|---|---|
| Move cards out of skills | ISC-1, ISC-2, ISC-3, ISC-5, ISC-19 | none | false |
| Catalog-onboard skill | ISC-4 | none | true |
| Onboarding detail and copy | ISC-6–16, ISC-20 | move | false |
| Company check requires the card | ISC-17, ISC-18 | copy | false |
| Docs and this ISA | ISC-21 | the rest | false |

## Decisions

- 2026-09-27: Independent read-only release audit found no critical scoped blocker; preserve explicit native/UI/Hermes pilot limits. Advisor invocation failed on configured 1M-context usage credits; no advisor endorsement or exhaustive secret scan is claimed.

- 2026-09-27: User authorized committing all completed work and creating a version-bumped release. Choose 0.6.0 for additive workflows with stricter exact-action approval behavior. Publish through PR checks, merge and a tag on the merged commit; runtime installation is separate.
- 2026-09-27: Original research packet matches the committed worktree copies; its index and ISA are superseded by cumulative records. Preserve original local bytes. Release edits are bounded metadata/documentation changes; no bulk coding dispatch is needed. Existing review agent performs independent release audit.

- 2026-09-22: Catalog cards stay in the repo and leave the profile skill path. Upstream packs are not vendored.
- 2026-09-22: Rows with an empty repo stay offered. The card says the cache has no URL.

- 2026-09-27: Research scope is the full 456-record local cache (444 at initial inspection) plus primary-source checks; failed sync prevents a claim of current X completeness. Broad scanning precedes manual curation. The framework retains reusable process; company facts require a company-owned promotion decision.
- 2026-09-27: Read-only noesis-observe advisor dispatched for architecture review. Native orchestration handles corpus inventory and documentation; no bulk coding or runtime changes are in scope.
- 2026-09-27: Final scan includes the independently updated 456-record cache. Own sync failed; full X refresh remains unverified. 92 candidate records, 36 curated, 44 shelf and 12 excluded.
- 2026-09-27: Advisor allegations about missing onboarding generation were refuted by scripts/onboard.py. Final advisor and conflict recall both failed on configured 1M-context credits; no advisor endorsement is claimed.


## Changelog

- 2026-09-27 | conjectured: the initial 444-record cache was the stable ingestion input.
  refuted by: the final corpus count check found 456 records and five additional candidates.
  learned: verify source-store freshness again before closing a research ingestion.
  criterion now: ISC-23 verifies the final snapshot count and the receipt separates observed refresh from own sync execution.

## Verification

Release preparation evidence, 2026-09-27:

- ISC-81: File read — distribution.yaml declares `version: 0.6.0`; English README badge agrees.
- ISC-82: File read — docs/releases/v0.6.0.md includes EN/FR features, install/upgrade path and native/UI/media/source limitations.
- ISC-83: Command — `Ran 300 tests ... OK`; Swift `Executed 9 tests, with 0 failures`; `Build complete!`; all seven media hashes and sizes verified. Hosted CI runs Python on Ubuntu; local Swift evidence is separate.
- ISC-86: SHA-256 — original ISA plus seven research files captured and compared unchanged; research packet is already in this branch and the index is a superset.
- Publication checks ISC-84 and ISC-85 occur after this source snapshot is committed; their authoritative evidence is the merged PR, remote main/tag refs and published GitHub release. No publication is claimed at preparation time.

`python3 -m unittest discover tests` — 10 tests, OK. `skills/catalog` is absent. `catalog/cards/openspec/SKILL.md` names Fission-AI/OpenSpec. 60 card directories. Pipe run of `onboard.py` exits 0 and prints SKILLS.

Research verification, 2026-09-27 (historical ISC-1–21 were not re-run):

- ISC-22: CLI — sync exited 1 with missing X CSRF cookie; recorded in sync-receipt.md.
- ISC-23: SQLite — final snapshot contains 456 rows; full regex re-scan exactly matches 92 manifest candidates.
- ISC-24: Python assertions — all 92 IDs are unique and URLs match source rows.
- ISC-25: SHA-256 — every stored article hash matches the live read-only source row at verification.
- ISC-26: Manifest read-back — 36 curated, 44 shelf, 12 excluded; all records have dispositions.
- ISC-27: File read-back — README maps human, company, framework, runtime, seats and doors to current files.
- ISC-28: File read-back — synthesis explicitly states confidence is not permission and identifies conflicting existing contracts.
- ISC-29: File read-back — implementation brief defines source, claim, synthesis, procedure, correction and run receipt records.
- ISC-30: File read-back — priority table names observable acceptance evidence for nine proposed work items.
- ISC-31: File read-back — sync receipt lists missing quoted article pointers and the newly observed Company Brain article.
- ISC-32: Git status — only ISA.md and docs/research/ change in this checkout; no company, connector, skill or runtime file changes.

Library mirror created with ft library create; verified by reading it back and comparing its content hash. Content and source inventory are research artifacts; future integration remains proposed. Fresh sync and linked-body completion remain pending authenticated retrieval.

## Implementation verification — 2026-09-27

ISC-33: GitHub CLI — 58 issues closed and project entries Done; plan state reconciled.
ISC-34–35: CLI — knowledge and checker tests verify immutable revisions, idempotency, indexed retrieval, provenance, conflicts and path containment.
ISC-36: CLI — exact approval tests reject high confidence, changed scope/payload and expired/forged/cross-company records.
ISC-37: CLI — correction and content tests verify reviewed replay, stale-page/conflict rejection and citation preservation.
ISC-38–39: CLI — typed shadow outcomes and verbatim context/fallback tests; no live Jev invocation.
ISC-40: CLI — full 222-test suite passes; 11 concrete synthetic demo checks pass; git diff --check passes.

All new criteria close on local evidence. Source/live/installed/external-action claims are excluded. Own FT refresh remains failed/pending authentication from the earlier research scope. Original checkout WIP preserved; managed branch holds implementation.

### Implementation learning

- conjectured: successful external worker status and passing worker tests would satisfy the execution contract.
  refuted by: no task-specific gateway correlation rows and review found overwritten revisions, loose index matching, insufficient correction checks and missing approval root binding.
  learned: fleet status is dispatch evidence; independent behavioral checks establish local implementation quality.
  criterion now: ISC-34–40 require real boundary tests and trial receipts; external provider attribution remains unresolved explicitly.

2026-09-27 follow-up: use seven cache-order records from the user-refreshed FT store. Processing and local intake are authorized; native Hermes runtime/profile activation is not inferred. Source-only verification separates installed from upstream capabilities.

## Latest-seven verification — 2026-09-27

ISC-41–47 verified locally: `specs/008-native-learning/verification.md`. 237 tests pass; full-cache disposable-company intake and repeat are byte-stable. Seven post IDs/hash records, 45 resolved shortlinks, 44 disabled repository candidates, native source audit and a reviewed `/learn` handoff are saved. Two missing X articles and the actual company/profile native learning pilot remain explicit future evidence. No native learning improvement is claimed.

## Bilingual ecosystem documentation

- [x] ISC-48: NotebookLM receives a versioned, curated Factor ecosystem source set.
- [x] ISC-49: English ecosystem guide is generated and downloaded from NotebookLM.
- [x] ISC-50: French ecosystem guide is generated and downloaded from NotebookLM.
- [x] ISC-51: English operator playbook is generated and downloaded from NotebookLM.
- [x] ISC-52: French operator playbook is generated and downloaded from NotebookLM.
- [x] ISC-53: All four documents preserve verified/planned boundaries and have generation receipts.

2026-09-27 documentation scope refined: only the Factor framework and its product integrations; seven curated NotebookLM source bundles exclude development-orchestration material. Four EN/FR reports requested; explicit notebook IDs prevent shared-context changes.

## Bilingual documentation verification — 2026-09-27

ISC-48–53 complete: four NotebookLM-generated EN/FR reports, preserved raw exports, reviewed derivatives, seven scoped source bundles and an editorial correction source. All four reviewed notes read back byte-identically from the restricted notebook. English disposable CLI example passed; French static review passed; extracted shell syntax checks were blocked and are not claimed. Evidence: docs/ecosystem/2026-09-27/verification.md.

## French visual documentation

- [x] ISC-54: Visual generation selects corrected Factor-only sources with explicit French language.
- [x] ISC-55: French framework slide deck is generated and downloaded.
- [x] ISC-56: French operations slide deck is generated and downloaded.
- [x] ISC-57: French video overview is generated and downloaded.
- [x] ISC-58: French architecture infographic is generated and downloaded.
- [x] ISC-59: French learning infographic is generated and downloaded.
- [x] ISC-60: Visual/media checks and generation receipts document results and limitations.

## French media verification — 2026-09-27

ISC-54–60 complete: five Factor-only French NotebookLM supports downloaded (two eight-slide decks in PDF/PPTX, one 309.731-second MP4 and two PNG infographics). Initial decks and images rejected and preserved; revised decks and images visually reviewed. Video fully decoded and visually sampled; narration was not independently reviewed. Minor labels and the required pilot-pending infographic caption remain documented. Thirteen export hashes verified, seven final files selected. Evidence: `docs/ecosystem/2026-09-27/media-fr/verification.md` and `delivery-manifest.json`. No framework code or runtime/profile configuration changed.

## Install-or-upgrade prompt

- [x] ISC-61: Root prompt-install.md contains a complete copyable coding-session prompt.
- [x] ISC-62: Fresh installation uses verified existing scaffold and profile commands.
- [x] ISC-63: Upgrade flow verifies recorded distribution source and preserves company/config state.
- [x] ISC-64: Doctor and Hermes gateway commands match installed CLI help.
- [x] ISC-65: Mac shell runner and optional doors are accurately separated from the listener.
- [x] ISC-66: Anti: prompt verification does not modify real profiles, services, or company data.
- [x] ISC-67: README links the prompt; shell examples parse and disposable intent smoke check passes.

2026-09-27 decision: listener means Hermes gateway, as clarified by the user. This task creates a reusable prompt, not a new daemon or installer implementation. Explicitly branch fresh versus existing state; preserve recorded-source semantics and shared gateway ownership. The source/install/runtime/end-to-end distinctions are independent acceptance claims.

## Install prompt verification — 2026-09-27

ISC-61–65: file read-back and installed Hermes v0.21.5 help/source confirm copyable boundaries, new-company shell runner, install/update source semantics, doctor/gateway lifecycle and the Mac runner. Independent read-only review identified and resolved fresh platform setup, existing coder binding, foreground lifetime and linked-state backup coverage.
ISC-66: this task invoked CLI help and a disposable local scaffold/intent check only; no real profile installation/update, doctor repair, gateway mutation or company write was performed.
ISC-67: all 16 shell blocks pass `sh -n`; README link exists; disposable scaffold → write_intent → intent_card passes with a spaced directory path. The prompt is verified documentation; a live fresh install/upgrade was not run or claimed.

- 2026-09-27 | conjectured: one install/update command sequence could cover each local setup.
  refuted by: installed Hermes update uses its recorded distribution source and gateway services may be shared.
  learned: reusable upgrade prompts must branch on provenance, existing profiles and service ownership.
  criterion now: ISC-63 and ISC-64 require those decisions before mutation.

## Bilingual onboarding and learning resources

- [x] ISC-68: Seven reviewed NotebookLM media files are bundled with verified hashes and portable paths.
- [x] ISC-69: Company language defaults to English and accepts only en/fr.
- [x] ISC-70: Explicit language persistence preserves unrelated company preferences.
- [x] ISC-71: CLI invocation language overrides do not silently change saved preferences.
- [x] ISC-72: Onboarding offers localized steps and an explicit resource listing/open action.
- [x] ISC-73: Native Mac interface offers EN/FR without changing canonical room/intent values.
- [x] ISC-74: Native resource selection validates local paths and opens only on user action.
- [x] ISC-75: Native package builds and preference/resource tests pass.
- [x] ISC-76: French harvest instructions preserve the headings required by the parser.
- [x] ISC-77: Hermes skills and Raycast entry points explain/use the shared language choice.
- [x] ISC-78: README and docs offer EN/FR navigation and valid portable asset links.
- [x] ISC-79: Anti: language/resource work activates no company connector, live profile or messaging service.
- [x] ISC-80: Integration tests and independent review verify default, persistence, invalid-state and resource-opening behavior.

2026-09-27 decision: language is a company preference in `preferences.json`, with a per-invocation CLI override and session-only Mac selection before choosing a company. Existing facts, catalog descriptions, source quotes and protocol identifiers are not translated. Guides have EN/FR variants; reviewed media currently remain French-only. Resource actions are on demand, without startup hooks or automatic tool activation.

ISC-68: SHA-256/size check — all seven `docs/assets/fr/` files match the accepted generation originals; manifest records repository-relative paths.

## Bilingual onboarding verification — 2026-09-27

ISC-69–72: 300 Python tests pass, including 63 focused onboarding cases; disposable CLI acceptance verifies saved FR, temporary EN override, seven resource paths and no intent side effect.
ISC-73–75: native production source wires localized selector/resources without schema changes; 9 production-target Swift tests and `swift build` pass. Disposable app launch observed, but Computer Use attachment timed out; visual menu acceptance remains follow-up UI-01, not claimed.
ISC-76–78: French harvest headings exactly match English; profile/skill language instructions, framework_root config guidance, Raycast wrappers and EN/FR learning/README paths verified. Seven bundled asset hashes match original reviewed exports.
ISC-79–80: no real profile/service/company activation; read-only review and disposable tests found and repaired persistence, invalid-state, localization and opener defects. Documentation: `docs/onboarding-verification.md`. Runtime Hermes response and Raycast GUI acceptance remain separate from local source validation.

- 2026-09-27 | conjectured: worker test success would prove native preference persistence.
  refuted by: review found swallowed save errors and tests copying helpers rather than calling production code.
  learned: acceptance must exercise the exact persistence and opening paths used by the product.
  criterion now: ISC-75 and ISC-80 require production-target tests plus explicit runtime-review limitations.
