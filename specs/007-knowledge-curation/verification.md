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

## Dispatch provenance

The requested temperance-parallel-dispatch skill ran three isolated noesis-execute tasks. All batch statuses were ok and produced substantive diffs, but matching gateway correlation/session receipts were absent. Attribution remains unresolved; initial code was independently rejected/reworked and validated on in-session non-Sol agents. See execution-receipt.md. Do not promote selected-seat banners or worker-reported test counts into provider proof.
