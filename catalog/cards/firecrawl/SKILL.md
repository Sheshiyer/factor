---
name: firecrawl
description: "Firecrawl. Crawl when Hermes web extract is not enough. Broad crawls wait for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# Firecrawl

Factor card for an upstream cli. This file is not a copy of that project.

## When to use

Crawl when Hermes web extract is not enough. Broad crawls wait for approval.

Load this only when `connectors/enabled.yaml` lists `firecrawl`.

## Source

- Bookmark `2071040656634732984`
- https://github.com/firecrawl/firecrawl
- Risk `medium`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `firecrawl` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/firecrawl/firecrawl`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
