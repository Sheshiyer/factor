---
name: taste-skill
description: "taste-skill. A taste skill for design judgment."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# taste-skill

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

A taste skill for design judgment.

Load this only when `connectors/enabled.yaml` lists `taste-skill`.

## Source

- Bookmark `2033322376440549682`
- https://github.com/Leonxlnx/taste-skill
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `taste-skill` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/Leonxlnx/taste-skill`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
