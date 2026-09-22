---
name: calcom
description: "Cal.com. Scheduling product. Creating or changing a booking waits for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# Cal.com

Factor card for an upstream cli. This file is not a copy of that project.

## When to use

Scheduling product. Creating or changing a booking waits for approval.

Load this only when `connectors/enabled.yaml` lists `calcom`.

## Source

- Bookmark `2097364320149725205`
- https://github.com/calcom/cal.com
- Risk `medium`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `calcom` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/calcom/cal.com`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
