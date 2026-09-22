---
name: codex-seat
description: Send code work to the Codex Hermes profile on a Kanban card, in a worktree.
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [codex, kanban, factor]
    related_skills: [open-card]
    config:
      - key: factor.codex_profile
        description: Hermes profile name whose model is Codex
        default: coder
        prompt: Codex profile name
---

# Codex seat

Use this when the outcome is a code change. This profile stays on Claude.

## Procedure

1. Confirm `factor.codex_profile` exists: `hermes profile show <name>`. If the command fails, stop and say the profile has not been created. Do not write the code here.
2. Open the card with `open-card`. Assignee is that profile. Workspace is `worktree`. The body names the repo path, the done check (test command or diff), and the files in play.
3. The Codex profile loads the bundled `codex` skill. The card's brief is self-contained. It includes paths, constraints, and done, and it does not refer to this chat.
4. When the card asks for review, read the diff and the done check. `request-changes` names the failure. Completion waits until the check has been run and its output is on the card.

## Verification

`hermes kanban show <id>` lists the Codex profile as assignee and `worktree` as the workspace.
