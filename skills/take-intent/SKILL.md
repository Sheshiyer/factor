---
name: take-intent
description: "Read a Factor intent file and open one card. Load instinct, then the index, then one page."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [intent, hermes, factor]
    related_skills: [company-context, open-card, jev-gate]
    requires_tools: [terminal]
    config:
      - key: factor.company_root
        description: Absolute path of the company repo this profile operates
        default: ""
        prompt: Company repo path
---

# Take an intent

Use this when a job is waiting in `io/intent.json`. The door may be mac, raycast, or hermes. The card does not change with the door.

## Procedure

1. Resolve `factor.company_root`. If it is empty, stop and ask for the path.
2. Read `<company>/io/intent.json`. If the file is missing, stop and name that path. Do not search for another intent.
3. Read `instinct.md`, then `wiki/index.md`. Open the one linked page whose line matches the sentence. Do not load the rest of the wiki, and do not copy it into Hermes session memory.
4. Open one card with `open-card`. The five fields are fixed:
   - Desk. The intent room.
   - Seat. `claude` for writing. `codex` only when the sentence is code.
   - Done. A draft in `output/` that cites the pages it read.
   - Read. `instinct.md` and that one wiki page.
   - Write. `output/`.
5. Request review before the card can complete. A draft is not a send.
6. If you were woken by a schedule, the room is numbers, and no line was crossed, send nothing.

## Verification

`hermes kanban show <id>` lists the room as the desk. The door is not a field on the card.
