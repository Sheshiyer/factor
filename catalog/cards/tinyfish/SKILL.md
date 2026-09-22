---
name: tinyfish
description: "TinyFish. Web automation MCP. The five-app post only names this one. Paid runs and logins wait for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# TinyFish

Factor card for an upstream mcp. This file is not a copy of that project.

## When to use

Web automation MCP. The five-app post only names this one. Paid runs and logins wait for approval.

Load this only when `connectors/enabled.yaml` lists `tinyfish`.

## Source

- Bookmark `2035178397648003507`
- https://github.com/tinyfish-io/tinyfish-mcp-server
- Risk `high`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `tinyfish` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/tinyfish-io/tinyfish-mcp-server`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
