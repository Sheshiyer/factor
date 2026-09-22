---
name: xmcp
description: "X MCP. X platform MCP. Reading can use Hermes x_search. Posting waits for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# X MCP

Factor card for an upstream mcp. This file is not a copy of that project.

## When to use

X platform MCP. Reading can use Hermes x_search. Posting waits for approval.

Load this only when `connectors/enabled.yaml` lists `xmcp`.

## Source

- Bookmark `2040937372909531286`
- https://github.com/xdevplatform/xmcp
- Risk `high`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `xmcp` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/xdevplatform/xmcp`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
