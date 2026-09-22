---
name: layers
description: "Layers. Design skill named in the design-agent list."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Layers

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Design skill named in the design-agent list.

Load this only when `connectors/enabled.yaml` lists `layers`.

## Source

- Bookmark `2075536512024994039`
- https://layers.jamiemill.com/
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `layers` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `No install command. The source is the site or the bookmark.`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
