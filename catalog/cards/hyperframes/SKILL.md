---
name: hyperframes
description: "Hyperframes. Video frames in the agent stack post."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Hyperframes

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Video frames in the agent stack post.

Load this only when `connectors/enabled.yaml` lists `hyperframes`.

## Source

- Bookmark `2100625120691720385`
- https://github.com/heygen-com/hyperframes
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `hyperframes` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/heygen-com/hyperframes`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
