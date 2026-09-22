---
name: pageindex
description: "PageIndex. Page-level index over long documents."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# PageIndex

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Page-level index over long documents.

Load this only when `connectors/enabled.yaml` lists `pageindex`.

## Source

- Bookmark `2100625120691720385`
- https://github.com/VectifyAI/PageIndex
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `pageindex` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/VectifyAI/PageIndex`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
