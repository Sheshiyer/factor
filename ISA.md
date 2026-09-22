---
project: factor
effort: E3
phase: complete
progress: 21/21
mode: algorithm
started: 2026-09-22
updated: 2026-09-22
---

# Factor

## Problem

The bookmark catalog is real, and a profile install would still load all 60 offered cards. They lived under `skills/`, which Hermes owns. The picker did not show risk, approval, or whether a repository exists, and a written choice did not place the card in the company repo.

## Vision

Skills, plugins, and other capabilities are three doors. A person or an agent opens one, reads the cost, and takes only what this company will use. The profile keeps the operator. The company keeps the choice.

## Out of Scope

Upstream skill bodies. A live Hermes profile install. Invented repository URLs. A curses dependency. Composio as a catalog row. Enabling shelf items.

## Principles

A tool the company did not choose does not sit in the agent's prompt. The human menu and the agent menu are the same registry.

## Constraints

Hermes profile install owns `skills/` at the repo root. Catalog cards stay outside that tree until onboarding copies a chosen card into a company repo. Stdlib only.

## Goal

A founder or an agent chooses offered skills, plugins, and other capabilities by category. The choice is written to that company's `connectors/enabled.yaml`, and only those cards are copied into that company's `skills/`.

## Criteria

- [x] ISC-1: `skills/catalog/` does not exist.
- [x] ISC-2: `catalog/cards/openspec/SKILL.md` exists and names `Fission-AI/OpenSpec`.
- [x] ISC-3: `catalog/cards/` contains one directory per registry row with disposition `add`.
- [x] ISC-4: `skills/catalog-onboard/SKILL.md` exists and names `scripts/onboard.py`.
- [x] ISC-5: `distribution.yaml` owns `skills` and does not own `catalog`.
- [x] ISC-6: `--json --category skills` exits 0 and every row has category skills.
- [x] ISC-7: That output includes `openspec` and excludes `refactoring-ui`.
- [x] ISC-8: `--json --category plugins` includes `refactoring-ui` and `pixelrag`.
- [x] ISC-9: `--json --category other` includes `tinyfish` and `firecrawl`.
- [x] ISC-10: `--json` contains no id `composio`.
- [x] ISC-11: `--text --category skills` prints `SKILLS` and does not print `PLUGINS`.
- [x] ISC-12: `--enable goose` exits non-zero and mentions shelf.
- [x] ISC-13: `--enable not-a-tool` exits non-zero and mentions unknown.
- [x] ISC-14: `--company` plus `--enable openspec` writes `enabled.yaml` and copies `skills/openspec/SKILL.md`.
- [x] ISC-15: That copied card contains the OpenSpec repository URL.
- [x] ISC-16: `--enable-category plugins` writes `refactoring-ui` and `pixelrag` and no skill id.
- [x] ISC-17: `check_company.py` reports a missing card when `openspec` is enabled without `skills/openspec/SKILL.md`.
- [x] ISC-18: A company with the copied card does not fail the connector check for that id.
- [x] ISC-19: Anti: `sync_catalog.py` does not recreate `skills/catalog/`.
- [x] ISC-20: Anti: a non-tty run with no flags exits 0 without reading stdin.
- [x] ISC-21: This file contains `## Goal` and `## Criteria`.

## Test Strategy

| ISC | Type | Check | Tool |
|---|---|---|---|
| 1–5, 19, 21 | file | path exists or is absent, and a string match | `rg` or unittest |
| 6–13, 20 | cli | onboard stdout and exit code, stdin not a tty | `python3 -m unittest` |
| 14–18 | cli | temp company, then onboard and check_company | `python3 -m unittest` |

## Features

| Name | Satisfies | Depends on | Parallelizable |
|---|---|---|---|
| Move cards out of skills | ISC-1, ISC-2, ISC-3, ISC-5, ISC-19 | none | false |
| Catalog-onboard skill | ISC-4 | none | true |
| Onboarding detail and copy | ISC-6–16, ISC-20 | move | false |
| Company check requires the card | ISC-17, ISC-18 | copy | false |
| Docs and this ISA | ISC-21 | the rest | false |

## Verification

`python3 -m unittest discover tests` — 10 tests, OK. `skills/catalog` is absent. `catalog/cards/openspec/SKILL.md` names Fission-AI/OpenSpec. 60 card directories. Pipe run of `onboard.py` exits 0 and prints SKILLS.

## Decisions

- 2026-09-22: Catalog cards stay in the repo and leave the profile skill path. Upstream packs are not vendored.
- 2026-09-22: Rows with an empty repo stay offered. The card says the cache has no URL.
