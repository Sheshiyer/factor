---
name: superpowers
description: "Superpowers. A development method: clarify, test, review. Read it before installing the whole pack."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Superpowers

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

A development method: clarify, test, review. Read it before installing the whole pack.

Load this only when `connectors/enabled.yaml` lists `superpowers`.

## Source

- Bookmark `2035915909966229733`
- https://github.com/obra/superpowers
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `superpowers` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/obra/superpowers`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
