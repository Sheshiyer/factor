---
name: graft
description: "Graft. Context compression beside Hermes. Hermes compression stays the default."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# Graft

Factor card for an upstream cli. This file is not a copy of that project.

## When to use

Context compression beside Hermes. Hermes compression stays the default.

Load this only when `connectors/enabled.yaml` lists `graft`.

## Source

- Bookmark `2091157554919280688`
- https://github.com/NanoNets/Graft
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `graft` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/NanoNets/Graft`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
