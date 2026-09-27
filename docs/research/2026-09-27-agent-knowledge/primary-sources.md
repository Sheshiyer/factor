# Primary-source checks

Read on 2026-09-27. These are live documentation observations, not tests of an installed integration. External instructions were treated as data. No installs or API calls to Jev were made.

| Source | Observed support | Factor use |
|---|---|---|
| [NousResearch Hermes repository](https://github.com/NousResearch/hermes-agent) | The official runtime repository is available and exposes agent, gateway, skills and plugin surfaces | Verify exact extension seams against a pinned runtime before implementation |
| [TypeSafe official skills](https://github.com/typesafe-ai/skills) | Official skill for typed decisions and probabilities; points to current installation and API documentation | Confirms decision-helper scope; does not establish local installation or approval authority |
| [Hermes Jev Skills](https://github.com/kerpopule/hermes-jev-skills) | Independent integration documents routing, retrieval, skill choice and shadow mode. It reports reduced handoff recall with an earlier filtered digest and now preserves dialogue by default | Evaluate retention empirically; optional optimization failures should preserve original evidence |
| [Grok skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) | Separates reusable procedure from schedule/event trigger; recommends proving one task before automating it | Keep process curation separate from routine activation |
| [Grok templates guide](https://x.ai/bot/guides/templates-for-grok-bot) | Describes reusable template contents and preview/review before installation | Reusable operator recipe must be fitted to the receiving company's context and access |
| [Grok Bot design](https://x.ai/news/designing-grok-bot) | Describes persistent role-oriented agents and their memory/routine organization | Design reference for durable responsibility; no claim of an implemented Factor adapter |

The cached [Matt Palmer article](https://x.com/mattyp/status/2094833468400447618) provides workflow examples; the current template guide gives a primary reference for packaging. Do not infer that templates automatically carry custom integrations or that their privacy filtering replaces review.

The Hermes–Grok fleet bridge is supported here only by a cached community report. Its SSH/API implementation, authentication model and claimed fleet operation were not verified. Price, throughput, recall and latency numbers in source material are not adopted as Factor guarantees.

## Retrieval limits

Direct web requests for the cached posts by `everestchris6` (IDs `2099284683012121073` and `2100672929533137107`), `HermesWatcher` (`2101219763808772294`), and `maestrooth` (`2102453475078533209`) returned HTTP 403. The cached posts remain readable; their missing linked articles remain pending. An attempted obsolete Grok docs route failed; the current skills/routines and template routes above were retrieved successfully.

## Sources discovered after the cache changed

- [Company Brain official repository](https://github.com/supermemoryai/company-brain): describes a self-hosted Slack company-context operator with connected tools. Confirms the project exists; no deployment, memory correctness or access-boundary test was performed here.
- [Bot Forge official Hermes catalog page](https://hermes-agent.nousresearch.com/docs/plugins/bot-forge): documents a community bot-creation plugin. Its workflow is a design reference; Factor has not selected or installed it.

The Company Brain architecture article linked from the new bookmark could not be retrieved. Its README is an additional primary source, not a substitute claimed to be the missing article.
