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
