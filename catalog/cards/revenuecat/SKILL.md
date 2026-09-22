---
name: revenuecat
description: "RevenueCat MCP. Subscriptions and entitlements. Billing writes wait for approval. No repository URL in the cache text."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, other, factor]
    related_skills: [connector-gate, company-context]
---

# RevenueCat MCP

Factor card for an upstream mcp. This file is not a copy of that project.

## When to use

Subscriptions and entitlements. Billing writes wait for approval. No repository URL in the cache text.

Load this only when `connectors/enabled.yaml` lists `revenuecat`.

## Source

- Bookmark `1981787308887253146`
- The bookmark cache does not include a repository URL.
- Risk `high`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `revenuecat` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `No install command. The source is the site or the bookmark.`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
