# Factor documentation corrections

The original NotebookLM reports are retained under `raw/`. The four top-level language documents are editorially reviewed derivatives. The following clarifications are grounded in the current framework code and the pinned Hermes source audit.

- `scripts/approvals.py make` returns an object with field `id`, not `approval_id`. A record captures a prior real human decision; its creation alone does not authenticate a person or permit an external executor. Disposable examples do not authorize publication.
- `scripts/content_trial.py` assembles supplied prose and attaches accepted source evidence. It does not verify semantic entailment of arbitrary prose or existing citations, generate prose, or create a structured three-angle field. A human or a future native workflow supplies and reviews those angles.
- Evidence blockers write a blocked review packet with `draft: null` and exit code 1. Invalid input, an unindexed target page, or a path error exits 2. The script does not discover every unreviewed statement in free-form prose.
- The executable correction store uses `wiki/corrections/<uuid>.json` and `wiki/proposals.json`. Acceptance appends a reviewed marker to the target page. `wiki/corrections.md` is the narrative log convention, not the JSON store written by `corrections.py`. Proposal is an explicit command after enough evidence; no native skill is automatically updated. Native `/learn` is a separate reviewed operation.
- A stale pending correction requires renewed human review of the changed page before accepting against its newly reviewed digest. Already accepted proposals cannot be accepted again.
- `scripts/snapshot.py` snapshots `instinct.md`, `profile-soul.md`, and `raw/`; it is not a whole-company, wiki, or native-skill backup. It does not itself run `check_company.py`. Native skill rollback needs its own versioned snapshot and verification.
- Native unattended destructive memory replace/remove operations are staged rather than directly applied, even if the general gate is disabled; staging failure denies the operation. That is a safeguard, distinct from the audited gate configuration/import fail-open limitations.
- 237 tests passed in the phase 008 local suite. The 5.285-second duration belongs to an earlier 222-test run and must not be attached to 237. Test counts do not establish installed-profile or live learning acceptance.
- Current missing X article bodies were unavailable in the selected cache/retrieval evidence. Their absence is not proven to be caused by the earlier agent sync authentication failure.
- A company/profile setup example is conditional on inspecting the selected existing environment. Source examples of Claude/Codex seats must include model selection before calling them configured. Room cadences are playbook contracts, not evidence of active schedules.
- No candidate repositories or schedules were activated by this work. The source audit did not establish the status of every other installed tool, profile or service on the user's computer.
- NotebookLM is an online documentation synthesis service. These reports are derived guides, not the controlling source contracts or authored claims by an invented professional identity.

Source references: `scripts/approvals.py`, `scripts/content_trial.py`, `scripts/corrections.py`, `scripts/snapshot.py`, `docs/seats.md`, `docs/hermes-learning-loop.md`, `docs/knowledge-curation.md`, `specs/008-native-learning/verification.md`, and the pinned native audit under `docs/research/2026-09-27-latest-seven/`.
