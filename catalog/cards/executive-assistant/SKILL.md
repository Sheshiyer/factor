---
name: executive-assistant
description: "Executive assistant skills. Inbox, calendar, and follow-up jobs. Port the jobs. Do not take the OpenClaw runtime. Sending waits for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Executive assistant skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Inbox, calendar, and follow-up jobs. Port the jobs. Do not take the OpenClaw runtime. Sending waits for approval.

Load this only when `connectors/enabled.yaml` lists `executive-assistant`.

## Source

- Bookmark `2029013122506223688`
- https://github.com/mgonto/executive-assistant-skills
- Risk `medium`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `executive-assistant` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/mgonto/executive-assistant-skills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
