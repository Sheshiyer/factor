---
name: html-video
description: "html-video. Local HTML-to-MP4. Hermes is one of the agents it detects."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# html-video

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Local HTML-to-MP4. Hermes is one of the agents it detects.

Load this only when `connectors/enabled.yaml` lists `html-video`.

## Source

- Bookmark `2062470358687498470`
- https://github.com/nexu-io/html-video
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `html-video` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/nexu-io/html-video`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
