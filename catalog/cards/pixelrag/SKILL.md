---
name: pixelrag
description: "PixelRAG. Reads a page from a screenshot. The cache text does not include a repository URL. Hermes vision plus browser covers the same job when this is off."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, plugins, factor]
    related_skills: [connector-gate, company-context]
---

# PixelRAG

Factor card for an upstream plugin. This file is not a copy of that project.

## When to use

Reads a page from a screenshot. The cache text does not include a repository URL. Hermes vision plus browser covers the same job when this is off.

Load this only when `connectors/enabled.yaml` lists `pixelrag`.

## Source

- Bookmark `2068639188396744937`
- The bookmark cache does not include a repository URL.
- Risk `medium`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `pixelrag` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `No install command. The source is the site or the bookmark.`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
