# Factor + Hermes: learning from work

Status: source-verified operating design; no native profile or learning write activated by this change. Installed Hermes source is 0.21.5 at `645da6561c724b7ca163d4af9c21de3a6397c9f2`. The [audit](research/2026-09-27-latest-seven/hermes-native-audit.md) pins the upstream comparison and distinguishes capability from effective profile settings.

Factor's local tools retain facts, evidence and company review. Hermes already provides procedural skills, bounded memory, session recall, `/learn`, conditional post-turn review and `/journey`. We use those native mechanisms instead of building another background learner. This is procedural/memory improvement, not model-weight training.

## What belongs where

| Information | Durable home | Change rule |
|---|---|---|
| Original posts/articles | FT cache; company source revisions when selected | Immutable content revision; missing body is explicit |
| Accepted factual claim | Company knowledge store/wiki | Source revision and locator; reviewed status |
| Private company voice/correction | Company page and correction record | Explicit acceptance against reviewed page digest |
| Short stable operating preference | Profile-local native memory | Review staged memory write; no copied corpus |
| Reusable procedure | Selected profile-local native skill and on-demand references | Native skill change reviewed and evaluated |
| Past conversation | Native session store, recalled through session_search | Stay within selected company/profile |
| Improvement evidence | Factor run and evaluation receipts | Compare prior/candidate versions on equivalent tasks |
| Send/spend/publish approval | Exact-action company approval | Independent of learning approval and model confidence |

## Start with one real job

Use the research-to-content brief: a founder-selected topic, 1–3 readable sources, three supported angles, one chosen outline and a cited draft. The first seven cache records in [this intake](research/2026-09-27-latest-seven/README.md) provide ideas for the method; a roundup alone does not substantiate the draft's business claims.

First run the bookmark intake in [dry-run mode](bookmark-ingest.md). Apply it only to the intended company root. Review factual claims separately. The current `content_trial.py` is a deterministic packet assembler for supplied text; it does not call Hermes or generate prose. During the later native pilot, Hermes can supply the proposed draft and Factor can check its evidence/corrections using that same local boundary.

## Native pilot preflight

Choose the exact company root and its Hermes profile. Use one writer per Hermes home. Inspect the effective profile configuration, selected skills and source version. Shared external skill directories and cross-profile session search can cross company boundaries; exclude them unless explicitly intended. Do not clone another company's memory into this pilot.

The following settings are supported in the pinned source and are a **configuration proposal**, not commands executed by this task. Replace the profile name with the actual company-specific profile before applying:

```yaml
memory:
  write_approval: true
skills:
  write_approval: true
auxiliary:
  background_review:
    enabled: false
    max_input_tokens: 48000
```

Keep background review disabled for the first manual `/learn` trial so every proposed change can be attributed to that run. Enable it only after the manual approval-and-replay path passes. The 48000-token bound is a proposed later review budget, not a Hermes default or a cost estimate. Review uses a model and can incur its normal cost. Notification settings affect visibility, not whether writes happen. Native gates default off; source inspection found unreadable/invalid gate config and one gate import failure can also leave them off. Verify effective gates before live work rather than trusting intended YAML. No runtime configuration has been changed here.

## Execute, learn, review, replay

1. **Execute the baseline.** Run one selected task, preserving input source revisions, output, tool failures, elapsed time and review edits. A failed or untested method does not graduate just because a bookmark recommends it.
2. **Classify feedback.** Wrong fact → claim/source review. Wrong voice → company correction. Repeated workflow failure → procedure candidate. Tiny durable preference → native memory proposal. Temporary run detail → session/run log. This prevents an ever-growing soul or a global memory dumping ground.
3. **Ask native `/learn` to distill demonstrated method.** Use the [reviewed-workflow prompt](../prompts/hermes-learn-reviewed-workflow.md). Supply the real successful run and correction examples. The agent writes through native `skill_manage`; it must not paste private source bodies into a shared skill.
4. **Review native pending writes.** In that same profile, use `/memory pending` and `/skills pending`; `/skills diff ID` shows a skill proposal. Approve or reject individual IDs after checking target, source scope, commands, tests and side effects. A pending ID must correspond to a persisted pending record; a returned ID alone is not proof. Native skill approval authorizes a skill change, not external actions.
5. **Start a fresh session and replay.** After approved bytes are verified, use a fresh session (`/new` on a gateway) or the appropriate reload. Run a held-out task that tests the lesson without repeating the exact example. Verify actual `skill_view`/tool usage and the resulting artifact. Native memory snapshots are session-bound; staying in one endless session weakens the recall/reuse test.
6. **Keep, revise or retire.** Record improvement and regressions. Restore the prior known-good skill if correctness, source isolation, voice constraints or authority worsens. Re-evaluate every proposed update.

Installed syntax (not invoked here): `/learn ...`, `/memory pending`, `/memory approve ID`, `/memory reject ID`, `/skills pending`, `/skills diff ID`, `/skills approve ID`, `/skills reject ID`, `/refine`, `/journey list`, `/reload-skills`. `/journey` is a CLI/TUI/Desktop visibility surface; do not assume it is a messaging command. See the audit for exact source references and platform differences.

## Self-improvement ownership

Background review is conditional, not a promise that every turn improves. It can propose memories and procedural changes when its triggers and tools permit. Foreground `/learn` skills are user-taught; they are not automatically owned by autonomous curation. Keep them user-owned during the pilot. The installed `hermes curator adopt NAME` can deliberately opt an eligible skill into curation later; it is not run or implied by ingestion. Canonical Factor operator skills should not be silently rewritten by a source-derived learning job.

Native skill approval replays operations; it does not provide a general reviewed-file digest check for all edits/deletes. Inspect the current target and proposed diff just before approval, snapshot the prior version, and replay tests. Factor's source/correction/action digest checks remain separate.

## How we know the system is learning

Use the same rubric before and after, plus at least one held-out case. Record these fields in a company run receipt; integration into native tool receipts remains the next implementation step:

```json
{
  "company_id": "explicit-company",
  "card_id": "explicit-card",
  "native_session_id": "from actual Hermes receipt",
  "skill_name": "selected-procedure",
  "skill_sha256_before": "measured",
  "skill_sha256_after": "measured",
  "source_revisions": [],
  "fixture_id": "held-out-example",
  "unsupported_claims": 0,
  "citation_failures": 0,
  "correction_recurred": false,
  "policy_regressions": 0,
  "human_edit_count": 0,
  "tool_failures": 0,
  "elapsed_seconds": null,
  "tokens": null,
  "decision": "keep|revise|retire"
}
```

This is a proposed receipt shape, not a fabricated run. Require zero unsupported claims, citation failures, cross-company retrieval and unauthorized actions. A held-out task must avoid the demonstrated correction while preserving unrelated requirements. Measure edit burden, cost and time; don't claim percentage improvement from a single successful fixture. `/journey` can show activity but cannot replace this comparison.

## Next product slice

A single review card should show evidence, missing sources, proposed lesson, native pending diff, before/after artifact and held-out result. Human and agent see the same chosen capability registry. After repeated manual success, add native scheduling with a budget, quiet unchanged-state behavior and a pause control. Bot Forge specialists or a different memory backend become candidates only when measured workflow failure justifies them.

Primary references: [Hermes memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory), [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [pinned source audit](research/2026-09-27-latest-seven/hermes-native-audit.md). Current results are local source/CLI evidence; a live Hermes improvement trial awaits the selected company/profile.
