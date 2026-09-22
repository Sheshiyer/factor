---
name: agent-reach
description: "Agent-Reach. Read-only reach across sites. Anything that posts waits for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# Agent-Reach

Factor card for an upstream cli. This file is not a copy of that project.

## When to use

Read-only reach across sites. Anything that posts waits for approval.

Load this only when `connectors/enabled.yaml` lists `agent-reach`.

## Source

- Bookmark `2101223518570488027`
- https://github.com/Panniantong/Agent-Reach
- Risk `medium`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `agent-reach` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/Panniantong/Agent-Reach`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
