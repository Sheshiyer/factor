---
name: translate-book
description: "translate-book. Book translation skill from the 20-skill stack."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# translate-book

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Book translation skill from the 20-skill stack.

Load this only when `connectors/enabled.yaml` lists `translate-book`.

## Source

- Bookmark `2101399836587331901`
- https://github.com/deusyu/translate-book
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `translate-book` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/deusyu/translate-book`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
