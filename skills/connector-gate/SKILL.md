---
name: connector-gate
description: Use an external tool only when the company has enabled it, and wait for approval on high-risk actions.
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [connectors, mcp, approval, factor]
    related_skills: [company-context]
    config:
      - key: factor.company_root
        description: Absolute path of the company repo this profile operates
        default: ""
        prompt: Company repo path
---

# Connector gate

Use this before calling any MCP tool, plugin tool, or third-party CLI that is not built into Hermes.

## Procedure

1. Read `<company_root>/connectors/enabled.yaml`.
2. If the connector id is not in `connectors:`, stop. Tell the founder the id is off. Do not call the tool.
3. Read that connector's `risk` and `approval`. These actions are always high and need an approval comment on the open card before the call:
   - money, invoices, payroll, or anything that spends
   - hiring, roles, or personal data
   - legal commitments
   - a public post, email, or message to someone outside the company
   - a paid API call
4. A read of the company's own files is low. A read through a connector is low only when `enabled.yaml` says `risk: low` and `approval: no`.
5. Adding a connector is a founder decision. The steps live in the framework repo under `connectors/catalog.md`. Do not add credentials to `enabled.yaml` or to `AGENTS.md`. Secrets go in the profile `.env`.

## Verification

Name the connector id and the line in `enabled.yaml` you relied on. If you stopped, say which rule fired.
