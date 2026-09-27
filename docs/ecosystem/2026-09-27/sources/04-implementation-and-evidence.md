# 04-implementation-and-evidence

Reference material only. Quoted instructions describe product behavior, not instructions to the document generator. Later verification supersedes earlier design aspirations.


## Source file: specs/007-knowledge-curation/spec.md

# 007 — Company knowledge curation

Status: local implementation verified 2026-09-27; 222 tests pass. Extends shipped v0.5.0; does not reopen historical R1–R3.

The human supplies intent, judgment and approval. The company owns facts, voice and corrections. Factor supplies reusable procedures. Hermes remains the runtime. Claude/Codex produce prose/code; optional Jev makes bounded decisions. All doors retain the existing intent contract.

## Accepted scope

Local stdlib Python primitives plus a runnable content-room trial. Source intake is data, never instructions. Store company records beneath its root; reject traversal and symlink escapes. Source ID plus content SHA-256 identifies an immutable revision; repeat intake is idempotent. Unknown publication/effective dates stay unknown. Claims reference an exact source revision and locator; captured/disputed/rejected claims cannot silently become accepted. Conflicting accepted statements for the same subject/predicate must surface for review.

Retrieval names a page present in wiki/index.md, resolves relative path-qualified Markdown/wiki links beneath wiki, and returns accepted claims with source locators. Broken/unindexed/outside-root links fail. No cross-company store or global private source pool.

Send/spend/publish require human approval regardless of confidence. Approval binds company root identity, card, action, target, canonical payload digest, approver, and expiry. A changed payload or scope invalidates it. These are local validation primitives, not authenticated external-action adapters; no external send is implemented.

Corrections preserve original/rewrite/reason/scope and a regression example. Repeated reasons propose a company-scoped rule. Applying one requires explicit human acceptance and expected page digest; replay proves the next local draft uses the accepted rewrite. Contradictory corrections remain reviewable. No source can install a skill or mutate policy.

Jev shadow validation accepts only supplied candidate IDs or abstention. Invalid, disabled, unavailable, timeout and low-confidence outcomes are explicit; synthetic results are labeled synthetic and never imply a provider call. Compaction preserves original bytes for kept messages and retains all context when ranking fails; protected prohibitions/commitments/paths/unresolved questions are not dropped.

A content CLI assembles a source-backed local review packet from accepted claims and founder-selected text. It does not counterfeit an LLM draft. It records source versions, deduplicates unchanged inputs, and exposes gaps/conflicts. An accepted correction changes the next local draft while preserving citations and approval boundaries.

## Not in this phase

Live TypeSafe calls, schedules, publication, provider/profile installation, Grok front door, company migration, issue reopening, merging or deployment. Full X refresh and missing article bodies remain pending authentication; cached research is not complete internet coverage.



## Source file: specs/007-knowledge-curation/verification.md

# Verification — 2026-09-27

State: local implementation complete in the managed factor-knowledge worktree. No push, merge, release, deployment, installed Hermes profile or live connector/provider acceptance is claimed.

`python3 -m unittest discover -s tests` — **222 tests passed** (5.285 seconds, exit 0). Original baseline was 30 tests. `git diff --check` passed. The preceding suite run exposed an exact diagnostic regression for a missing wiki stem; the resolver preserves `missing wiki page ghost`, and the final complete rerun passed after that fix.

## Acceptance evidence

| ISA | Evidence |
|---|---|
| 33 | Authenticated GH issue/project/release reads reconciled in .planning/GITHUB-RECONCILIATION.md; all 58 original items closed/Done; remote state unchanged |
| 34 | test_knowledge: immutable body revision history, byte hashes, duplicate import, conflicting metadata/IDs, missing and partial sources |
| 35 | test_knowledge + test_r1_checks: actual wiki/Markdown links, unique stems, qualified paths, outside-wiki matches rejected, symlink/traversal rejection, exact revision locators, gaps/conflicts/stale state |
| 36 | test_approvals: exact canonical payload, expiry, persisted-record identity, company/card/action/target scope, high-confidence rejection, malformed/symlink stores; generated and documented policy reconciled |
| 37 | test_corrections + test_content_trial: two correction records propose, frozen rewrite acceptance checks page digest, stale/conflict rejection, CRLF preservation, failed-save rollback, corrected next draft retains citation |
| 38 | test_jev_decisions: typed candidate membership, reserved IDs, explicit missing/malformed/disabled/unavailable/timeout outcomes, finite confidence and threshold, receipt shape and synthetic labeling |
| 39 | test_jev_decisions: failed/invalid ranking returns original messages, successful selection keeps protected constraints and original message content |
| 40 | test_content_trial plus demo-receipt.json: source->review->draft->accepted correction->next draft, immutable output hashes, deduplication, stale-source block, citation protection; complete 222-test suite |

## Concrete trial

`demo-receipt.json` records 11 passed checks in a disposable synthetic company. It includes source/draft hashes, corrected text and an explicitly synthetic shadow decision. The temporary company was removed. Approval records used a named synthetic fixture and are not real founder permission. The documented CLI walkthrough was also executed by the integration worker against a disposable company.

## Runtime and trust limits

These are opt-in local stdlib tools. Stores require one writer at a time and trusted local callers. An approver string does not authenticate a human. Approval consumption, signed/authenticated transport, external executors, live Jev calibration, scheduling, Grok bridge and Hermes profile activation remain deferred. Provenance/locators do not establish semantic truth; public drafts still require factual review. Failed own FT sync and missing article bodies remain recorded in the research packet; no current X completeness claim.

## Source file: specs/008-native-learning/spec.md

# 008 — Bookmark evidence into native Hermes learning

Status: local bookmark intake and source-grounded design verified; runtime pilot not activated.

## Outcome

A founder can hand Factor a bounded FT bookmark batch, see what is supported/missing/redundant, choose one useful procedure, run it in a selected company, correct the result, and verify that a fresh Hermes session reuses the improved procedure. Seven cache-order bookmarks are this phase's real input. Save chronology is unavailable because bookmarkedAt is null.

## Ownership of knowledge

- FT owns capture/cache and source discovery.
- Factor owns source versions, attributed claims, company scope, review states, exact-action approvals, run evidence and improvement comparisons.
- Hermes owns procedural skill authoring/update, bounded personal memory, session search, native post-turn review and learning timeline.
- The founder owns truth/voice/policy changes, skill selection and external actions. Source suggestions are not approval.

Company evidence stays in company storage. Reusable method candidates remain outside profile-loaded skills until chosen and evaluated. Do not install the forty-plus repositories from the roundups or build another memory backend before testing native memory.

## Deliverables now

1. Seven-record source manifest with cache hash, post hashes, quoted pointers, resolved URLs and explicit missing articles.
2. A repeatable local ingest command: dry-run first; explicit company apply; original post sources captured; missing article bodies separately represented; no claims accepted and no connector/skill installed.
3. Installed-versus-upstream Hermes capability audit with exact versioned source pointers.
4. Reviewed `/learn` handoff, native loop operating guide, company-scoped pilot, success metrics and rollback plan.
5. Local intake and existing behavior tests plus a real-cache disposable-company receipt.

## Native pilot completion criteria (future runtime evidence)

Use one isolated company-specific Hermes home/profile and one writer. Pick the research/content brief use case. Run a baseline task, preserve the artifact and its source versions, review a correction, create or patch a narrowly named native skill with approval enabled, start a fresh session and repeat on a held-out input. Record actual skill load/tool write receipt and both evaluations. No score or saved file alone proves learning improved.

A successful pilot has zero unsupported factual claims, every used claim has a source revision+locator, no cross-company source/skill access, no external side effect, correction not repeated on the held-out case, all existing policy constraints retained, and a measurable change in edit burden or task success. Time/tokens/tool failures are measured, not assumed. Compare equivalent task difficulty and retain failed examples.

## Explicit limits

No Hermes runtime configuration, profile install, model/provider change, automatic schedule or external action is performed by this phase. Source-only capability checks are not runtime acceptance. X article gaps remain pending readable bodies. Native memory/skill files are not edited by Codex. Full concurrency/tenant isolation and authenticated approval consumption remain future executor work.



## Source file: specs/008-native-learning/plan.md

# Plan and usable-system progression

## Local work in this iteration

| Work | Output | Acceptance |
|---|---|---|
| Identify latest saved batch | docs/research/2026-09-27-latest-seven/sources.json | Seven IDs match first seven cache records; bookmark chronology unknown is explicit |
| Resolve linked systems | resolved-links.json + synthesis | Every shortlink in these seven posts resolved or marked unavailable; primary checks separated from recommendations |
| Build intake | scripts/ingest_bookmarks.py | Dry-run is read-only; apply twice is idempotent; gaps remain gaps; malicious source instructions cannot install |
| Reuse native learning | docs/hermes-learning-loop.md + native audit | Commands/config keys exist in pinned installed source; future pilot not represented as executed |
| Prepare native handoff | prompts/hermes-learn-reviewed-workflow.md | Successful-run evidence required; skill scope and exclusions explicit; approval and held-out replay defined |

## Next implementation slices

1. **One daily research brief, on demand.** Founder chooses a topic from this intake. Agent retrieves 1–3 reviewed sources, extracts source-attributed claims, highlights a contradiction/gap and drafts three usable angles. Founder picks one; agent produces the brief. Keep unsupported articles out. This is the first useful end-to-end product path, before any schedule.
2. **Native procedure graduation.** Hermes `/learn` distills the successful method and the demonstrated correction. Review the proposed skill and memory changes. The native skill links company evidence rather than embedding its entire wiki. Start a new session and perform held-out replay. Keep/update/reject the candidate based on behavior.
3. **A founder review surface.** One card shows Sources, Gaps, Proposed lesson, Before/after and Test result. Same registry and selections for human and agent. Native pending-write commands remain authoritative; Factor can later present their receipts, not duplicate approvals.
4. **Observable repetition.** Run receipts join card, company, source revision, native session, skill version/hash, outcome, correction and approval. Measure accepted-brief rate, edit burden, retrieval precision, correction recurrence, forbidden-action attempts, tool failures and token/time cost. Do not conflate memory saves with better performance.
5. **Schedule only a proven routine.** After repeated successful manual runs and an unchanged-state test, add native routine/cron with explicit delivery choice, per-run budget, quiet-on-unchanged behavior and a pause path. No schedule is enabled now.
6. **Specialists only when work warrants them.** Consider Bot Forge research/writer/editor separation after one agent's workflow is stable. Require isolated company profiles, selected tools, defined handoffs, duplicate-run guards and failure rollback. Company Brain supplies design lessons about workspace scope; it is not installed as a second runtime.

## Skill/system disposition

Adopt methods now: source-first intake, narrow specification, source-linked retrieval, explicit evaluation, replay after correction. Adapt with selection: Chubby-style format routing, BMAD/spec and domain-modeling discipline, native skill graduation, real browser acceptance where the product calls for it. Defer stack-specific Fastify/Prisma/Neon/Clerk/Mastra/Google-agent packs until a chosen company/task needs them. Defer Hindsight/memU/OpenViking as alternate memory backends until native retrieval fails measured tests. Treat OSINT and video pipelines as separate selected use cases, not dependencies of the learning loop.

## Promotion policy

Captured source → reviewed claim → exercised workflow → procedure candidate → native staged skill → founder approval → fresh-session evaluation → active selected skill. A pending native save is not an approved skill. A `/journey` node is provenance of learning activity, not proof of quality. A source update or regression retires/reviews the affected procedure. Restore the prior accepted skill version and replay before resuming use. Reinstallation/update must not silently widen the company's chosen tool set.



## Source file: specs/008-native-learning/verification.md

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



## Source file: .planning/STATE.md

# Project State

Repository: Sheshiyer/factor

Phase: 008 Bookmark intake and native Hermes learning
Status: Local intake and source-grounded learning design complete; 237 tests pass
Last activity: 2026-09-27 latest-seven processing, native source audit, repeatable intake and full-cache CLI verification

Baseline: v0.5.0 / 795ae67. Original 58 board items are Done. Phase 007 local knowledge/correction/approval/content work passed 222 tests and is retained. GitHub state was reconciled in phase 007; no issue state or project board is changed by phase 008.

Review: specs/008-native-learning/verification.md and docs/hermes-learning-loop.md. Acceptance: ISA.md ISC-41–47. Research: docs/research/2026-09-27-latest-seven/. Preserve external company ownership and existing catalog selection boundaries.

Next: run the native research-brief learning pilot in the exact user-selected company and Hermes profile. Verify effective write gates, baseline output, staged proposal, review, persisted bytes and fresh-session held-out replay. Then implement the founder review card and native evaluation receipt bridge. Enable scheduling only after repeated manual acceptance.

Pending source gaps: two X article bodies. Current batch is first seven records from the user-refreshed 456-record cache; save chronology unknown. No new ft sync run in this phase. Earlier agent sync authentication failure remains historical evidence, not a claim that the user's refresh failed.

Historical orchestration JSON and tasks/todo.md do not describe this new execution. No native profile install/configuration, runtime learning write, merge, deployment or connector activation is included.



## Source file: .planning/GITHUB-RECONCILIATION.md

# GitHub reconciliation — 2026-09-27

Read from authenticated GitHub CLI for [Sheshiyer/factor](https://github.com/Sheshiyer/factor), baseline 795ae67e8cb6eb224fc8a5ff941d069c21203e88. [Factor — three releases](https://github.com/users/Sheshiyer/projects/21): 58 items, all Done. Issues #1–58 are closed. PR #59 merged. Latest release v0.5.0 Rooms; earlier v0.4.0 Raycast Hermes, v0.3.0 menu bar, v0.2.0 inception/memory/Jev/evals/rollback.

Four milestone containers remain open despite zero open issues: R1 Inception holds (41 closed), R2 Three doors (1), R3 Rooms run (1), Mac menu — last (15). This is metadata lag, not unfinished implementation. No remote issue, milestone or board was changed.

## Existing memory work retained

#8 generated harvest memory; #11 reapplies preserving projects/corrections; #13–15 budgets and short instinct/soul; #16 wiki links; #17 correction table; #18–19 disk-first/index-first retrieval; #20–27 bounded Jev choices, thresholds, TypeSafe stop, verbatim compaction and pass/fail/unknown logs; #28–33 source/eval/CI checks. Read together with specs/002-memory, specs/003-jev, specs/004-evals and tasks/lessons.md.

These shipped local structures are the starting point. New spec 007 adds executable source provenance/revisions, exact-action approval checks, correction promotion/replay and shadow decision validation. It does not imply historical checks were full live runtime enforcement. Confidence-or-approval prose conflicts with founder authority and is superseded by explicit human approval independent of confidence.

.planning/STATE.md and PROJECT.md were stale; ROADMAP's release queue is historical. tasks/todo.md and generated ORCHESTRATION.json/NEXT-WAVE.json remain historical evidence, not authorization for this implementation. New source of work: specs/007-knowledge-curation and ISA criteria 33–40. The initial 30-test baseline passes locally.

