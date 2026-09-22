---
name: email-marketing-bible
description: "email-marketing-bible. Email marketing. Sending waits for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# email-marketing-bible

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Email marketing. Sending waits for approval.

Load this only when `connectors/enabled.yaml` lists `email-marketing-bible`.

## Source

- Bookmark `2101399836587331901`
- https://github.com/CosmoBlk/email-marketing-bible
- Risk `high`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `email-marketing-bible` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/CosmoBlk/email-marketing-bible`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
