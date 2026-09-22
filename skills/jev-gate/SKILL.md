---
name: jev-gate
description: "Use Jev only to pick, score, or say yes or no. Options come from files. Jev does not write drafts, prices, or claims."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [jev, eval, factor]
    related_skills: [company-context, open-card, connector-gate]
---

# Jev gate

Use this when a job needs a choice, a score, or a confidence. Claude and Codex still write the sentences.

## When it is allowed

The options already exist in a file.

- Which room, from content, numbers, growth, ads, partners, money, or the desk in `departments/`.
- Which wiki page, from the lines in `wiki/index.md`.
- Does this draft need a person. Yes or no, plus a confidence from 0 to 1.
- Does this tool call still matter. Keep the original text, or drop it. Do not rewrite it into a summary.

## Thresholds

- Under 0.5, stop and ask Claude or the founder.
- 0.85 or above before a send, a spend, or a publish. Otherwise wait for an approval comment.
- Record pass, fail, or could not tell as one line in `wiki/log.md`.

## When it is missing

If the TypeSafe skill is not installed, stop. Tell the founder:

`npx skills add typesafe-ai/skills --skill typesafe-ai`

Do not answer the choice with Claude or Codex and call it Jev.

## Never

Do not let Jev invent options, write prose, name a price, or state a claim. A number in `output/` must already appear in `wiki/` or `context/`.
