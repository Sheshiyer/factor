---
name: open-card
description: Open a Hermes Kanban card for one piece of company work, with a seat, a done test, and the files it may read.
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [kanban, company, factor]
    related_skills: [company-context, codex-seat]
    requires_tools: [terminal]
---

# Open a card

Use this when work should move on the board instead of happening inside the chat.

## Procedure

1. Load `company-context` first. If a required context file is still `FILL:`, do not open the card.
2. One card is one outcome. Title it as the outcome.
3. Create it with `hermes kanban create`. Put the body in a file and pass `--body-file` so newlines survive.
4. The body has five parts, in this order:
   - Desk. The department folder, or `context` when no department exists yet.
   - Seat. `claude` for judgment and writing. `codex` for code. See the `codex-seat` skill before assigning code.
   - Done. The check that proves it, named so someone else can run it.
   - Read. Absolute paths under the company root. Nothing else.
   - Write. The one file or directory the work may change.
5. Writing and review cards assign to this profile. Code cards assign to the Codex profile and use `--workspace worktree`.
6. Link follow-up work with `hermes kanban link`. A later desk does not start until the parent card is complete.
7. Anything public, paid, or hard to undo is created with the founder as the reviewer. Do not `complete` that card yourself.
8. A card is finished when a review says ship. The worker's own "done" is not the stop. Request review before completion. Drafts are drafted. They are not sent.

## Verification

Show the task id from `hermes kanban create`, then `hermes kanban show <id>` and confirm the five parts are in the body.
