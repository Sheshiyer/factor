---
name: awesome-mcp
description: "awesome-mcp-servers. A directory of MCP servers. Pick one server. Do not enable the directory."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# awesome-mcp-servers

Factor card for an upstream catalog. This file is not a copy of that project.

## When to use

A directory of MCP servers. Pick one server. Do not enable the directory.

Load this only when `connectors/enabled.yaml` lists `awesome-mcp`.

## Source

- Bookmark `2096252768633995734`
- https://github.com/punkpeye/awesome-mcp-servers
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `awesome-mcp` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/punkpeye/awesome-mcp-servers`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
