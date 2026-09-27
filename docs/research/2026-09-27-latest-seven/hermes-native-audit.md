# Hermes native learning audit for Factor

Verified 2026-09-27. Read-only source investigation; the only written artifact is this report. No profile configuration, memories, sessions, secrets, logs, provider calls, scheduled jobs, skills, or runtime state were read or changed. Source capability is not installed-profile enablement or successful runtime execution.

## Version receipt and upstream comparison

- Installed checkout: `/Users/sheshnarayaniyer/.hermes/hermes-agent`; `git status --short` returned empty.
- Installed HEAD: `645da6561c724b7ca163d4af9c21de3a6397c9f2`, commit dated `2026-09-24T11:13:26-04:00`, subject `fix(desktop): let the cloud ladder own the reauth logout`. `git describe --tags --always` returned `645da6561c` (no reachable descriptive release tag).
- Installed source package version: **0.21.5**, both `pyproject.toml:5` and `hermes_cli/__init__.py:6`.
- Official upstream main observed by `git ls-remote https://github.com/NousResearch/hermes-agent.git HEAD refs/heads/main`: **806fa64fd87b34e1d4838280db29c5a3d57040bc**.
- Official GitHub compare API reports main **3181 commits ahead, 0 behind** the installed commit. This is commit distance, not 3181 relevant learning changes. The compare endpoint caps its changed-file list; targeted files were therefore fetched separately via official GitHub Contents API at the exact upstream SHA and compared in memory.
- At that upstream SHA, `hermes_cli/__init__.py` no longer hardcodes a semver: it declares release date `2026.9.24`, exposes lazy `__version__` derived from an install stamp, with `0.0.0` fallback. Do not call upstream “0.21.5” or recommend an update purely from its number.

Targeted exact-source comparisons:

| File | Installed vs upstream | Material finding |
|---|---|---|
| `agent/learn_prompt.py` | Byte-identical | Native `/learn` already installed |
| `hermes_cli/commands.py` | Byte-identical | Same learn/journey/approval command registry |
| `tools/session_search_tool.py` | Byte-identical | Same history search/read/scroll API |
| `tools/skill_manager_guards.py` | Byte-identical | Same native ownership/read-before-write guards |
| `hermes_cli/write_approval_commands.py` | Byte-identical | Same approval replay/review handlers |
| `website/docs/user-guide/features/memory.md` | Byte-identical | Same documented learning controls |
| `tools/write_approval.py` | Changed | UTF-8 BOM-aware reads and equivalent exception handling; gate semantics retained |
| `tools/skill_manager_tool.py` | Changed | `hermes_yaml`, BOM-aware reads, generic profile creation-path wording instead of dynamic schema path; no new learning engine required |
| `hermes_cli/profiles.py` | Changed | Runtime/install bucket exclusion changes, BOM/YAML handling, active-profile read changes; broader upgrade deserves a separate review |
| `website/docs/user-guide/features/skills.md` | Changed | New Desktop browse/install explanation; corrects old installer `--no-skills` claim. Named-profile `hermes profile create NAME --no-skills` remains documented |
| `agent/background_review.py` | Compare patch reviewed | Adds review cache-fork tag to isolate diverged xAI slot cache |
| `agent/learning_graph.py` | Compare patch reviewed | BOM-aware skill/usage reads |
| `agent/turn_finalizer.py` | Compare patch reviewed | Interruption, silent-stop, and post-compaction read-cache fixes; these are runtime reliability differences, not missing native learning |

Official immutable source roots: [installed commit](https://github.com/NousResearch/hermes-agent/tree/645da6561c724b7ca163d4af9c21de3a6397c9f2), [upstream inspected commit](https://github.com/NousResearch/hermes-agent/tree/806fa64fd87b34e1d4838280db29c5a3d57040bc), [compare](https://github.com/NousResearch/hermes-agent/compare/645da6561c724b7ca163d4af9c21de3a6397c9f2...806fa64fd87b34e1d4838280db29c5a3d57040bc).

## The genuine native loop already present

1. Hermes has profile-local curated memory and session persistence. `session_search` searches actual SQLite FTS5 history and returns messages; it is not an LLM-generated recollection or a source intake engine. Its four argument shapes are search (`query`), read (`session_id`), scroll (`session_id` plus `around_message_id`), and recent browse (no query). It supports explicit `profile`, date filters, and excluded sessions. Do not use cross-profile search as an accidental cross-company knowledge pool. Source: `tools/session_search_tool.py:619,652`.
2. During real work, `skill_view` loads procedures; `skill_manage` can create/edit/patch/delete skills and write/remove support files. Its advertised operations batch applies atomically, with legacy flat calls still supported. Skills remain procedural files; this is not model-weight training. Source: `tools/skill_manager_tool.py:776,878`, `tools/skill_manager_batch.py`.
3. `/learn <sources and requirements>` composes a standards-guided prompt and queues a normal agent turn. The agent reads sources with its existing tools and authors via `skill_manage`. Empty `/learn` asks it to distill the workflow just completed. The source hygiene explicitly treats retrieved text as data and strips hidden directional/control instructions. Large corpora use a lean SKILL.md plus topic reference files, rather than a second ingestion service. Source: `agent/learn_prompt.py:1,122,136`; `hermes_cli/cli_commands_mixin.py:1925`.
4. Post-turn background review is genuine installed behavior, but conditional. Memory review ticks on user turns; skill review ticks on tool iterations and requires `skill_manage`. A completed, uninterrupted final response and non-suppressed review are required. Source: `agent/turn_context.py:709`; `agent/turn_finalizer.py:682-710`. Thus “every turn always self-improves” is inaccurate.
5. Review uses the main model and warm conversation by default; a different configured model receives a digest. Same-model review inherits main-model reasoning; routing to a distinct model is needed for separate reasoning effort. Review forks disable their own review nudges. Source: `agent/background_review.py:150-222,822,990`; installed memory docs at lines 358-425.
6. Changes pass native memory/skill write gates when enabled. `/journey` renders observed learned/used skills and memory cards; it is a visibility surface, not a quality score, factual verifier, or proof that a procedure succeeded. Sources: `agent/learning_graph.py:194-211`; `hermes_cli/journey.py:16,344`; memory docs lines 246-264.

## Supported configuration and commands

These keys exist in the installed source and the inspected upstream sources. The actual installed Factor profile settings were deliberately not read; the Factor framework `config.yaml` currently sets only `kanban.dispatch_in_gateway: true`, so the repository itself does not yet request learning write approval.

| Config key | Installed behavior/default |
|---|---|
| `memory.memory_enabled` | true; built-in MEMORY.md store |
| `memory.user_profile_enabled` | true; built-in USER.md store |
| `memory.memory_char_limit` / `memory.user_char_limit` | 2200 / 1375 characters |
| `memory.write_approval` | false by default; true gates foreground and background memory writes |
| `skills.write_approval` | false by default; true stages skill writes from either origin |
| `memory.nudge_interval` | 10 user turns; 0 suppresses automatic memory nudge |
| `skills.creation_nudge_interval` | 10 tool iterations; 0 suppresses skill nudge |
| `auxiliary.background_review.enabled` | true; false disables automatic forks, manual `/refine` still supported |
| `auxiliary.background_review.provider` / `.model` | route review; auto/default uses main model |
| `auxiliary.background_review.reasoning_effort` | applies for different-model route; ignored for same-model route |
| `auxiliary.background_review.max_input_tokens` | aggregate replayed input budget; <=0 unlimited; unset uses 75% of context, capped 600000, fallback 120000 |
| `auxiliary.background_review.extra_tools` | default []; only already-available tools can be added to review whitelist |
| `auxiliary.background_review.defer` / `.defer_max_age_s` | auto / 1800; managed local server idle deferral; `never` opts out |
| `display.memory_notifications` | off/on/verbose; gateway notification display only, does not stop writes |
| `skills.create_dir` | optional destination for newly authored skills; avoid sharing across companies |

Sources: `hermes_cli/config_defaults.py:1289-1302`; `agent/agent_init.py:1264-1288,1342-1344`; `agent/background_review.py:150-222`; `website/docs/user-guide/features/memory.md:270-505`; skills docs lines 415-429.

Commands below are verified syntax, **not executed**:

```sh
hermes -p factor config set memory.write_approval true
hermes -p factor config set skills.write_approval true
hermes -p factor config set auxiliary.background_review.enabled true
hermes -p factor config set auxiliary.background_review.max_input_tokens 48000
hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company
```

In the intended profile's chat:

```text
/learn the reviewed local Factor workflow at PATH, preserve company isolation and evidence requirements
/memory pending
/memory approve ID
/memory reject ID
/memory approval on
/skills pending
/skills diff ID
/skills approve ID
/skills reject ID
/skills approval on
/refine
/journey list
/reload-skills
```

Memory foreground writes may prompt inline in interactive CLI; elsewhere and for background reviews they stage. Skill writes always stage when gated. `/memory` and skill approval subcommands work in messaging; `/journey` is CLI/TUI/Desktop, not messaging. `/learn` is available across CLI/gateway/TUI/dashboard. Avoid `approve all` for learning from heterogeneous bookmarks.

Profile commands already supported: `hermes profile install /path/to/factor --name factor --alias`; `hermes profile create coder --no-skills --description "..."`; `hermes -p factor ...`. Profiles isolate config, skills, memories, sessions and DB; shared external directories deliberately relax that boundary. `--clone` copies curated memory, so it is unsuitable as an unquestioned clean company sandbox. Sources: `website/docs/reference/profile-commands.md:73-100`; `website/docs/user-guide/profiles.md:7-17,80-96`; Factor `docs/seats.md`.

## Important limits of native approval

Native approval is useful consent workflow, not equivalent to Factor's digest-bound action authorization.

- `tools/write_approval.py:43-59` treats invalid/unreadable gate configuration as gate off. `tools/skill_manager_tool.py:627-636` also fails open if its gate import fails. Explicitly inspect actual gate state before a live trial; do not claim a hard security boundary from intended YAML alone.
- Pending skills store operation arguments and replay through `apply_skill_pending`; the reviewed implementation does not bind full edit/delete operations to a reviewed file digest. Patch matching supplies some protection, but is not a general stale-content compare-and-swap. Sources: `tools/skill_manager_tool.py:646-676`; `hermes_cli/write_approval_commands.py:122-137`.
- Memory replace/remove has separate exact-target pinning and rejects stale or unpinned legacy targets. Do not generalize that protection to all skill operations.
- A staging write disk failure logs the failure and returns staging metadata without committing the target; a returned pending ID alone is insufficient persistence proof. Source: `tools/write_approval.py:75-92`.
- Autonomous curation cannot rewrite user-owned, external, bundled or hub-installed skills under the native ownership guard. Foreground `/learn` creations are user-taught, not automatically curator-owned. `hermes curator adopt NAME` opts an eligible skill into ownership for curation; adoption is a separate deliberate action. Exact-target read-before-write is enforced for background edits. Sources: `tools/skill_manager_guards.py:180-232`; `tools/skill_usage.py:523`; `agent/curator.py`.

## Factor integration: native learning plus company evidence

Factor should retain the new deterministic company layer and use Hermes for agent learning. Do not build a duplicate session search, memory daemon, background learner, skill registry, journey graph, or `/learn` ingestion engine.

- `scripts/knowledge.py:211-355`: retain immutable source revisions, exact claim locators, explicit captured/accepted/disputed/rejected review, wiki index containment, stale evidence and conflicts. Hermes session history and a learned SKILL.md are not substitutes for these facts.
- `scripts/corrections.py:106-255`: retain company/page-scoped original/rewrite/reason/regression evidence, repeated evidence proposals, explicit human acceptance against exact page digest, and frozen accepted rewrite pairs. A native memory save is not equivalent to accepted company policy.
- `scripts/content_trial.py:98-175`: retain deterministic review packets, protected citation text, source revisions, gaps/conflicts and content digests. Use Hermes to draft when explicitly desired, then feed the proposed draft through this local evidence/review path. Do not describe the present local assembler as an LLM draft or a native-learning runtime test.
- Promote a **reusable procedure**, such as source -> capture claim -> human review -> trial -> correction -> replay, into a profile-local Hermes skill. Company facts and private bookmark bodies stay under that company root, referenced by the procedure; do not bake them into a shared/global skill.
- Newly fetched bookmark/article content enters captured evidence first. Missing bodies and unknown dates stay explicit. A source URL or marketing claim cannot instruct `/learn` to change policy or invoke external actions. Human review of the source-derived procedure remains distinct from accepting its underlying factual claims.
- Keep `scripts/approvals.py` and send/spend/publish human authority separate. Hermes skill approval authorizes a skill file change, not external publication or payment.

## Concrete graduation and evaluation conditions

Recommended staged acceptance, not yet executed:

1. Use a disposable company and a dedicated Hermes test profile; avoid cloning private memories. Verify exact profile identity, source revision, effective config and both approval gates before model work.
2. Feed a reviewed local workflow to native `/learn`; inspect `/skills pending` and `/skills diff ID`. Confirm target profile, no copied credentials/private company facts, supported commands, source references, and absence of prompt-injected policies. Reject rather than approve any unsafe result.
3. Execute candidate procedure in that disposable environment under explicit test authorization. Test the positive sequence and adversarial cases: missing body, unknown date, rejected claim, stale revision, conflict, path escape, stale page digest, changed action payload, citation preservation, repeated correction and deduplication.
4. Demonstrate that a staged candidate has no effect before approval. After explicit human skill approval, verify the actual persisted bytes, reload skills or open a fresh session, and replay an independent fixture. Require the corrected next draft, unchanged unrelated text/citations, correct company identity and zero unauthorized external actions.
5. Record parent/provider/model, candidate skill hash, input fixture hashes, results and approved revision. Separate source tests, native tool execution and runtime provider evidence. Journey visibility is supplementary evidence only.
6. Keep learned skills user-owned initially. Only opt into autonomous curation after sustained successful independent replays and an explicit ownership decision; protect canonical Factor framework skills from automatic rewriting. Preserve a known-good skill snapshot for rollback and rerun evaluation after every proposed update.

These are integration criteria proposed from the inspected contracts. No live Hermes learning invocation, profile installation, background review, skill activation, curator adoption or provider capability was verified in this audit.

Official live references also consulted: [persistent memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory), [skills system](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [upstream write approval implementation](https://github.com/NousResearch/hermes-agent/blob/806fa64fd87b34e1d4838280db29c5a3d57040bc/tools/write_approval.py). Installed source references above resolve relative to `/Users/sheshnarayaniyer/.hermes/hermes-agent`; Factor references resolve relative to `/Users/sheshnarayaniyer/.codex/worktrees/factor-knowledge/factor`.

## Ready-to-review pilot fragment and exact preflight

Proposed **test-profile** config fragment only; not applied:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: true
  nudge_interval: 10
skills:
  write_approval: true
  creation_nudge_interval: 10
auxiliary:
  background_review:
    enabled: false
    max_input_tokens: 48000
    extra_tools: []
```

Start with automatic background review disabled while validating manual `/learn` and `/refine`; after those pass, changing only `auxiliary.background_review.enabled` to `true` is the separate automatic-loop pilot step. This keeps the trial attributable and bounded. Do not put a top-level `background_review` block in the config. Provider/model are deliberately omitted, which uses the profile's existing main route rather than selecting or activating a new provider.

Next-session preflight: verify the exact selected disposable profile; check both effective gate values are actual enabled booleans and the gate module imports. A missing, malformed or unreadable config is a stop condition even though native gate fallback permits writing. Inspect only selected keys rather than dumping config or credentials. Supported key reads:

```sh
hermes -p factor-learning-test config get memory.write_approval
hermes -p factor-learning-test config get skills.write_approval
hermes -p factor-learning-test config get auxiliary.background_review.enabled
hermes -p factor-learning-test config get auxiliary.background_review.max_input_tokens
hermes -p factor-learning-test curator status
hermes -p factor-learning-test curator list-unmanaged
```

In that profile's chat, `/memory approval` and `/skills approval` report gate state; require ON for each. `/memory pending` and `/skills pending` list staged writes without accepting them. Prove one harmless synthetic candidate stages and exists in the pending listing, while the actual skill/memory target remains unchanged. This is required before using bookmark-derived material; a “staged” response alone is insufficient. No pilot preflight was executed this turn.

Supported fresh-session and review commands are `/new`, `/skills diff ID`, `/skills approve ID`, `/skills reject ID`, `/memory approve ID`, `/memory reject ID`, `/reload-skills`. `/new` creates a fresh session/history; it does not erase profile memory or skills. Sources: installed `hermes_cli/commands.py:55,124,245,262`; `hermes_cli/write_approval_commands.py:35-62`.

Exact curator CLI surface, all deliberately unexecuted:

```sh
hermes -p factor-learning-test curator status
hermes -p factor-learning-test curator list-unmanaged
hermes -p factor-learning-test curator adopt SKILL --dry-run
hermes -p factor-learning-test curator adopt SKILL
hermes -p factor-learning-test curator pin SKILL
hermes -p factor-learning-test curator unpin SKILL
hermes -p factor-learning-test curator pause
hermes -p factor-learning-test curator resume
hermes -p factor-learning-test curator run --dry-run
```

Adoption changes provenance/ownership and makes an eligible user-taught skill subject to curator lifecycle handling; pinning controls automatic transitions. Neither is a quality evaluation. Do not run adoption, unpinning, resume or a live curator pass merely to inspect state. `/learn` output should remain user-owned during the first pilot. CLI parser supports adoption and list-unmanaged even though the shorter `/curator` completion registry lists fewer options; use the CLI spelling above for exactness. Source: `hermes_cli/curator.py:606-650`.

Additional fail-open detail: `tools/memory_tool.py:84-91` also allows normal writes if importing the write-approval module fails. Its separate unattended replace/remove guard (`tools/memory_tool.py:164-190`) stages destructive background memory edits even with the general gate off. These distinct mechanisms must not be conflated.
