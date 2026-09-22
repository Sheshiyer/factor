---
name: openspec
description: "OpenSpec. Spec-first change proposals before implementation."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# OpenSpec

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Spec-first change proposals before implementation.

Load this only when `connectors/enabled.yaml` lists `openspec`.

## Source

- Bookmark `2100625120691720385`
- https://github.com/Fission-AI/OpenSpec
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `openspec` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/Fission-AI/OpenSpec`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
