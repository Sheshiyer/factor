---
name: refactoring-ui
description: "Refactoring UI plugin. Polish pass based on Refactoring UI, from the design-agent list."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, plugins, factor]
    related_skills: [connector-gate, company-context]
---

# Refactoring UI plugin

Factor card for an upstream plugin. This file is not a copy of that project.

## When to use

Polish pass based on Refactoring UI, from the design-agent list.

Load this only when `connectors/enabled.yaml` lists `refactoring-ui`.

## Source

- Bookmark `2075536512024994039`
- https://github.com/gnurio/refactoring-ui-plugin
- Risk `low`. Approval `no`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `refactoring-ui` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/gnurio/refactoring-ui-plugin`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
