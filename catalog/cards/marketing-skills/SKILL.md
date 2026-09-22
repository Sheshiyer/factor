---
name: marketing-skills
description: "Marketing Skills. Product-marketing skills: SEO, email, social, pricing, churn. Sending and ads wait for approval."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, skills, factor]
    related_skills: [connector-gate, company-context]
---

# Marketing Skills

Factor card for an upstream skill. This file is not a copy of that project.

## When to use

Product-marketing skills: SEO, email, social, pricing, churn. Sending and ads wait for approval.

Load this only when `connectors/enabled.yaml` lists `marketing-skills`.

## Source

- Bookmark `2035841006273548481`
- https://github.com/coreyhaines31/marketingskills
- Risk `medium`. Approval `yes`.
- Public sends, spend, and paid calls wait for an approval comment even when approval is no.

## Procedure

1. Load `connector-gate` and confirm `marketing-skills` is enabled.
2. If the upstream is not installed, give the founder this command and stop:

   `npx skills add https://github.com/coreyhaines31/marketingskills`

3. Read the upstream before running it. Follow its own instructions for the task.
4. Write results into the company repo path named on the card. Do not invent company facts.
