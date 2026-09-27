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
