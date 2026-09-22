---
name: markitdown
description: "MarkItDown. Office, PDF, and audio files into markdown for the company repo."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# MarkItDown

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Office, PDF, and audio files into markdown for the company repo.

Load this only when `connectors/enabled.yaml` lists `markitdown`.

## Source

- Bookmark `2090476415661830285`
- https://github.com/microsoft/markitdown
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `markitdown` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/microsoft/markitdown`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
