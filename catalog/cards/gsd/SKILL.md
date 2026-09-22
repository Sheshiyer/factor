---
name: gsd
description: "Get Shit Done. Planning and execution skills for a coding agent."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Get Shit Done

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Planning and execution skills for a coding agent.

Load this only when `connectors/enabled.yaml` lists `gsd`.

## Source

- Bookmark `2035915909966229733`
- https://github.com/gsd-build/get-shit-done
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `gsd` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/gsd-build/get-shit-done`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
