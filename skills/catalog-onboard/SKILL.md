---
name: catalog-onboard
description: "Choose Factor skills, plugins, and other capabilities for one company. Use scripts/onboard.py. Do not load the whole catalog into the profile."
version: 0.1.0
author: Thoughtseed
license: MIT
metadata:
  hermes:
    tags: [catalog, onboarding, factor]
    related_skills: [connector-gate, company-context]
    config:
      - key: factor.company_root
        description: Absolute path of the company repo this profile operates
        default: ""
        prompt: Company repo path
---

# Catalog onboarding

Use this when the founder wants to turn tools on or off for the company.

The profile does not carry the bookmark cards. They live in `catalog/cards/` of the Factor repo. Onboarding copies only the chosen cards into the company repo.

## Procedure

Onboarding has four steps. Do them in order. `python3 scripts/onboard.py --steps` prints the same list.

1. Harvest. The founder pastes a prompt into the project they have already been building. Claude gets `prompts/harvest-claude.md`. Codex gets `prompts/harvest-codex.md`. Print the prompt with `python3 scripts/onboard.py --prompt claude` or `--prompt codex`. The seat saves `factor-harvest.md` in that project. It does not invent missing facts.
2. Apply. This writes `<company>/SOUL.md`, the six context files, and the business and brand folders. `raw/harvest.md` is the archive. `wiki/index.md` is the catalog to read first. `wiki/entities/` and `wiki/concepts/` are the business. `brand/` is voice, proof, and the lock. SOUL.md is who the owner is and how the business sounds.

   `python3 scripts/onboard.py --company <company_root> --apply-harvest <project>/factor-harvest.md`

3. Choose. Show skills, then plugins, then other capabilities. Enable the one skill the desk will actually run. A longer list waits. A pile of unused skills is how the agent starts routing work to the wrong place.

   `python3 scripts/onboard.py --text --category skills`

   Enable only ids they name:

   `python3 scripts/onboard.py --company <company_root> --enable id,id`

4. Confirm. Read `<company_root>/SOUL.md`, the context files, and `connectors/enabled.yaml`. Each enabled id has `<company_root>/skills/<id>/SKILL.md`. Load `connector-gate` before calling any of those tools. Shelf ids are refused. Do not add them by hand.

## Verification

`enabled.yaml` lists the chosen ids, and each chosen id has a skill card in the company repo. The Factor profile skill list does not include `openspec` unless this company enabled it and that card was installed separately.
