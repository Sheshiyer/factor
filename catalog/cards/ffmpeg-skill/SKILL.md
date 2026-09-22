---
name: ffmpeg-skill
description: "FFmpeg skill. Local video edits: crop, captions, Ken Burns, silence cut. Does not publish."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# FFmpeg skill

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Local video edits: crop, captions, Ken Burns, silence cut. Does not publish.

Load this only when `connectors/enabled.yaml` lists `ffmpeg-skill`.

## Source

- Bookmark `2096964158994755604`
- https://github.com/kajisho5/ffmpeg-skill
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `ffmpeg-skill` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/kajisho5/ffmpeg-skill`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
