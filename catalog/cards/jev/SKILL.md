---
name: jev
description: "TypeSafe Jev. Yes/no and score calls. Not a third model seat. Install with npx skills add typesafe-ai/skills --skill typesafe-ai."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# TypeSafe Jev

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Yes/no and score calls. Not a third model seat. Install with npx skills add typesafe-ai/skills --skill typesafe-ai.

Load this only when `connectors/enabled.yaml` lists `jev`.

## Source

- Bookmark `2100917158922387537`
- https://github.com/typesafe-ai/skills
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `jev` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/typesafe-ai/skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
