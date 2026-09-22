---
name: color-expert
description: "color-expert. Color skill from the 20-skill stack."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# color-expert

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Color skill from the 20-skill stack.

Load this only when `connectors/enabled.yaml` lists `color-expert`.

## Source

- Bookmark `2101399836587331901`
- https://github.com/meodai/skill.color-expert
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `color-expert` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/meodai/skill.color-expert`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
