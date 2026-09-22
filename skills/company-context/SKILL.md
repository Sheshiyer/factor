---
name: company-context
description: Read a Factor company repo and stop when a context file is still unfilled.
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [company, context, factor]
    related_skills: [open-card, connector-gate]
    config:
      - key: factor.company_root
        description: Absolute path of the company repo this profile operates
        default: ""
        prompt: Company repo path
---

# Company context

Use this when a task needs to know what the company is, who it serves, or what it may claim.

## When to use

Any card, draft, or answer that depends on the business. Load it before writing.

## Procedure

1. Resolve `factor.company_root` from the skill config block injected with this skill. If it is empty, stop and ask for the absolute path. Do not search the disk for a likely repo.
2. Read `SOUL.md` in the company root first, then `wiki/index.md`. Open a linked page only when its line matches the card. Then read these files, and only these, unless the card names more:
   - `context/company.md`
   - `context/customer.md`
   - `context/offer.md`
   - `context/positioning.md`
   - `context/voice.md`
   - `context/proof.md`
3. If a file is missing, or any line contains `FILL:`, stop. Name the path and the missing fact. Leave the draft unwritten.
4. Treat `context/proof.md` as the only source of claims. A claim with no line there stays out of the draft.
5. Match `brand/style-dna.md` and `brand/lock.md` on anything a person outside the company might read. A draft that breaks a locked line does not ship. `context/voice.md` is the sample behind those two files.

## Verification

Quote the path you read for each fact you use. If you stopped, the message names the file and the `FILL:` line.
