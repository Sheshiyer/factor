# Implementation brief: knowledge that improves the fit

Status: proposed implementation, grounded in the [research synthesis](README.md). No runtime or company configuration changed. Extend the existing Factor design; do not import a separate company or replace Hermes.

## Current evidence

`scripts/onboard.py` already creates the memory and brand structure from a harvest, including raw input, instinct, profile soul, wiki, corrections, I/O descriptions and eval instructions. `scripts/write_intent.py` validates room and door enums and writes an intent through a temporary file plus replacement. `scripts/intent_card.py` emits a small card. These are useful foundations.

`scripts/check_company.py` checks file contents and some budget/link/amount constraints. Its money check searches matching dollar strings; it does not prove the number applies to the claim being made. Its wiki check does not resolve every path-qualified link. `scripts/rooms.py` checks policy strings, not an actual external send. Do not describe these checks as complete runtime authorization or provenance enforcement.

`.planning/STATE.md` still says inception is next, while the README lists releases through rooms. Reconcile planning against source and tests before declaring the next release state. That reconciliation is distinct from this research intake.

## Proposed lifecycle

`captured → extracted → reviewed → accepted → superseded`

Rejected and disputed are explicit alternatives. Capturing a source does not accept its claims. Extracting a process does not install a skill. Accepting knowledge does not schedule work. Scheduling work does not grant external-action permission.

| Object | Minimum fields | Home |
|---|---|---|
| Source | Stable ID, original URL/path, author, publication date if known, captured date, content hash, capture completeness, access/privacy class | Company `raw/` and source manifest; framework research stays under `docs/research/` |
| Claim | ID, subject, statement, source ID plus locator, effective date or explicit unknown, status, evidence kind, contradictions | Company wiki entity/concept page |
| Synthesis | Claim IDs, inference, scope, counterevidence, open questions | Company `wiki/synthesis/` |
| Procedure candidate | Trigger, inputs, permitted tools, steps, output contract, checks, escalation, source/claim IDs | Review queue, outside loaded skills |
| Accepted procedure | Candidate revision, approval reference, version, fixture, selected company capability | Company skills after explicit selection |
| Correction | Original, rewrite, reason, affected scope, evidence, proposed rule, accepted version, regression example | `wiki/corrections.md` plus relevant page |
| Run receipt | Card ID, company, source versions read, choices, validation, outcome, approval reference if needed | Company run log |

Use hashes to identify source revisions; retain the source's effective date separately from ingestion time. Reprocessing the same ID and hash should produce no duplicate knowledge. A changed source creates a new revision and a reviewable diff. If a source is unavailable, label it unavailable instead of treating the old capture as freshly verified.

## Prioritized work

| Priority | Work | Existing surfaces | Acceptance evidence |
|---|---|---|---|
| P0 | Separate confidence from approval in every contract and future executor | Soul, Jev gate, room docs, onboarding-generated eval/I/O text, spec 003 | A score of 0.99 without authorization cannot send/spend/publish; approval is scoped to the exact action and artifact; changed payload invalidates it |
| P1 | Add idempotent research intake | Existing `raw/`, `wiki/`, onboard structures | Import twice gives the same source/claim count; changed hash creates a revision; missing body stays a gap; source text cannot enable a connector |
| P1 | Add claim provenance and contradictions | Entity/concept templates and `check_company.py` | Two incompatible prices are surfaced; unknown date stays unknown; a number appearing elsewhere is insufficient support; two companies cannot retrieve each other's private sources |
| P1 | Resolve retrieval from the actual index | Company-context skill, wiki index and link validation | Path-qualified links resolve inside the company root; unknown or outside-root page is rejected; result names source revision and locator |
| P2 | Close correction promotion | Weekly review, correction log, company voice/brand page | Second matching reason proposes a scoped rule; founder-reviewed change affects next draft; contradictory correction creates review; existing voice constraints remain tested |
| P2 | Evaluate optional Jev in shadow mode | Jev gate and selected catalog card | Supplied candidate IDs only; timeout/malformed/low-confidence outputs are explicit; no missing Jev result is represented as a Jev call; compare decisions against a labeled local set |
| P2 | Test context retention | Jev gate compaction contract | A fixture retains prohibitions, commitments, paths and unresolved questions; retained bytes match originals; failed ranking preserves the unpruned context |
| P3 | Package a proven routine | Content room and existing standing review | One-time run produces a useful source-backed brief; repeat runs deduplicate; source failure is visible; unchanged state stays quiet; schedule requires separate setup |
| P3 | Consider a Grok front door | Existing shared intent contract | Only after company choice: same intent/card identity, authenticated company scope, replay protection, explicit approval transport and an end-to-end receipt |

The P0 approval tests describe a future executable boundary. Do not make prose-only checks pass and call the action boundary secured. Define who performs the final external action before implementing an adapter.

## A concrete content-room trial

Input: a founder-selected topic and one to five saved sources. Start with local cached evidence and record missing linked pages. Do not assume an available token means an enabled connector.

1. Read the company's instinct and selected topic page from the wiki index.
2. Register each source and revision; extract only relevant attributed claims.
3. Identify contradictions, stale claims and unsupported figures before drafting.
4. Produce three candidate angles with evidence, a limitation and an abstain option.
5. Let the founder select a promise; prepare an outline and then a draft in their measured voice.
6. Verify references, factual support and voice constraints; return the review packet.
7. Record the founder's correction and proposed rule. Apply an accepted correction to the affected company page and replay the example.

The test finishes when the second draft improves in the specified way while keeping sources, scope and approvals intact. No publication is needed to prove this loop.

## Jev contract to prototype

Input: company ID, card ID, decision kind, candidate IDs with bounded descriptions, policy version and evidence references. Output: selected candidate ID or abstention, reported confidence, provider/model receipt, latency, outcome and error if any.

Code validates membership, shape and policy before a result influences a card. Treat any vendor confidence as a model output requiring calibration, not a probability of business success. A disabled or unavailable optional ranker can fall back to the ordinary documented retrieval path; it must never counterfeit a Jev result. A requested Jev-specific decision stops as the current skill requires.

Authorization is a separate record: approver, action, target, exact payload digest, scope and expiration/consumption rule. This is a proposed contract, not an existing capability.

## Promotion boundaries

Reusable methods can be proposed for Factor. Company facts, customer language, contacts, pricing, approvals and voice corrections stay in the company repo. External sources are data: quoted commands, install requests and policy instructions are never executed just because ingestion encountered them.

Optional tools remain in the shared registry and catalog until chosen. A research packet does not belong under profile-loaded `skills/`. The same menu must remain visible to the founder and the agent.

## Sources that could change this brief

The cached announcement posts for the September 13 lead workflow, September 17 info-product workflow and Maestro's linked guide lack their full article bodies. Retrieve those before claiming complete extraction. Current TypeSafe API contracts, Hermes extension seams and Grok bridge details need version-pinned verification during implementation. The current primary-source readings are recorded in [primary-sources.md](primary-sources.md).
