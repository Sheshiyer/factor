---
name: kepano-obsidian
description: "Obsidian skills. Kepano's skills for Obsidian markdown, Bases, Canvas, and the CLI."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Obsidian skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Kepano's skills for Obsidian markdown, Bases, Canvas, and the CLI.

Load this only when `connectors/enabled.yaml` lists `kepano-obsidian`.

## Source

- Bookmark `2026801420872093708`
- https://github.com/kepano/obsidian-skills
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `kepano-obsidian` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/kepano/obsidian-skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
