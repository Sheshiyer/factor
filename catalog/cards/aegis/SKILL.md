---
name: aegis
description: "Aegis. Named in the 20-skill stack. Read the repo before trusting it."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Aegis

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Named in the 20-skill stack. Read the repo before trusting it.

Load this only when `connectors/enabled.yaml` lists `aegis`.

## Source

- Bookmark `2101399836587331901`
- https://github.com/GanyuanRan/Aegis
- Risk `medium`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `aegis` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/GanyuanRan/Aegis`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
