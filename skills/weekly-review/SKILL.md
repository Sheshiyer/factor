---
name: weekly-review
description: Monday review of open Factor cards. One message. Silent when nothing needs the founder.
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [blueprint, kanban, review, factor]
    related_skills: [company-context, open-card]
    blueprint:
      schedule: "0 9 * * 1"
      deliver: origin
      prompt: "Load the weekly-review skill. Review the Factor board for the company in factor.company_root. Deliver one short message only when a card is blocked, a review is waiting, or a context file should change. If nothing needs the founder, send nothing."
    config:
      - key: factor.company_root
        description: Absolute path of the company repo this profile operates
        default: ""
        prompt: Company repo path
---

# Weekly review

Use this on Monday, or when the founder asks how the company work is going.

## Procedure

1. If `factor.company_root` is empty, stop and ask for it. Do not review a guessed repo.
2. Run `hermes kanban list` and `hermes kanban stats`.
3. For each open card, note the desk, the seat, and whether done can be checked.
4. A blocked card, a card waiting on review, or a second failed run belongs in the message.
5. If the founder corrected a draft since the last review, append a row to `wiki/corrections.md`: the original line, the rewrite, and the reason. Name the voice or style file that should change. Do not edit it in this pass. The same reason twice means that file changes before the next draft.
6. A card that is moving and needs nothing gets one line at most, or silence.
7. If every card is healthy, do not deliver a message.

## Verification

The message, when there is one, names task ids. It does not retell the company's whole strategy.
