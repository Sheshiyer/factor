---
name: agent-skills
description: "Agent Skills. Production engineering skills. Install one workflow, not the whole tree."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Agent Skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Production engineering skills. Install one workflow, not the whole tree.

Load this only when `connectors/enabled.yaml` lists `agent-skills`.

## Source

- Bookmark `2096252768633995734`
- https://github.com/addyosmani/agent-skills
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `agent-skills` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/addyosmani/agent-skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
