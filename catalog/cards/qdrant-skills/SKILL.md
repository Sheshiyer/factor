---
name: qdrant-skills
description: "qdrant-skills. Qdrant skills. The company repo stays the source of record."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# qdrant-skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Qdrant skills. The company repo stays the source of record.

Load this only when `connectors/enabled.yaml` lists `qdrant-skills`.

## Source

- Bookmark `2101399836587331901`
- https://github.com/qdrant/skills
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `qdrant-skills` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/qdrant/skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
