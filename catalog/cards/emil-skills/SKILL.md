---
name: emil-skills
description: "Emil Kowalski skills. Design-agent skills from Emil Kowalski."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Emil Kowalski skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Design-agent skills from Emil Kowalski.

Load this only when `connectors/enabled.yaml` lists `emil-skills`.

## Source

- Bookmark `2075536512024994039`
- https://github.com/emilkowalski/skills
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `emil-skills` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/emilkowalski/skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
