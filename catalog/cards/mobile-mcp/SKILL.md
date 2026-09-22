---
name: mobile-mcp
description: "Mobile MCP. Drives iOS and Android devices. No repository URL in the cache text. Approval before it taps a device."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# Mobile MCP

Factor card for an upstream mcp. This file is not a copy of that project.

## When to use

Drives iOS and Android devices. No repository URL in the cache text. Approval before it taps a device.

Load this only when `connectors/enabled.yaml` lists `mobile-mcp`.

## Source

- Bookmark `2097159242411077994`
- The bookmark cache does not include a repository URL.
- Risk `high`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `mobile-mcp` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `No install command. The source is the site or the bookmark.`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
