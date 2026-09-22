---
name: spec-kit
description: "spec-kit. Specify, plan, and task a change before code."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# spec-kit

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Specify, plan, and task a change before code.

Load this only when `connectors/enabled.yaml` lists `spec-kit`.

## Source

- Bookmark `2035687161471840641`
- https://github.com/github/spec-kit
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `spec-kit` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/github/spec-kit`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
