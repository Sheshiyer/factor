# 01-factor-architecture

Reference material only. Quoted instructions describe product behavior, not instructions to the document generator. Later verification supersedes earlier design aspirations.


## Source file: README.md

<div align="center">



# Factor

One employee for the work that does not need you.<br>
You keep the decisions.

</div>

<!-- readme-gen:start:badges -->
<div align="center">

![Version](https://img.shields.io/badge/version-0.5.0-blue?style=for-the-badge)
![License](https://img.shields.io/github/license/Sheshiyer/factor?style=for-the-badge)

</div>
<!-- readme-gen:end:badges -->

You already do the jobs. Content, numbers, growth, ads, partners, money. A pile of prompts made that a second job: remember the task, start it, paste the context, check the result, move it to the next tool.

Factor takes the job. You say it in plain language. The employee reads the business, does the work, and comes back with a finished draft. Research, checking, and drafting run on their own. Sending, spending, and publishing wait until you say so.



## One intent, three doors

The same employee answers from the Mac menu bar, from Raycast, and from Hermes. The door is only where you speak. The job is the same sentence wherever you are.

| Door | What you do |
|---|---|
| Menu bar | Say the job without opening a project. `apps/mac/run.sh`. Unsigned and local. |
| Raycast | Say the job from the command bar. Add `surfaces/raycast`. |
| Hermes | Say the job from the chat you already use. The `take-intent` skill reads the intent and opens one card. |

Each door writes the same file: the sentence, the room, and the door. The card does not change with the door.



## The rooms

Start with one room. Content or numbers. They are frequent, easy to check, and nothing leaves the building. Add growth and ads when you trust the drafts. Add partners and money last. Those rooms send messages or spend.

| Room | What is waiting | Your part |
|---|---|---|
| Content | A researched list, on weekday mornings | Keep, drop, or develop |
| Numbers | The figures that matter | Decide what to change |
| Growth | A short list with evidence, once a week | Pick what to build |
| Ads | Only a campaign that crossed a line you set | Approve the change |
| Partners | A vetted list and the briefs | Choose who is asked |
| Money | Invoices and the week, already drafted | Send or hold |

A healthy room is quiet. You do not check every campaign. You see the one that changed. Content brings a short list and does not publish it. Numbers stay silent when no line was crossed. Partners and money draft, then wait for one yes.



## Instinct, and a memory that does not fill up

Hermes remembers a little, and that little fills. Factor does not put the company there.

**Instinct** is the pocket notebook. Who the owner is, how the voice measures, and what is locked. It loads every time. It stays short.

**Memory** is the card catalog. The wiki, the brand, and the correction log live on disk. The employee reads the index, then the one page the job needs. A correction is written down as the original line, the rewrite, and the reason. The same reason twice proposes a rule for your review. Accepted rules improve the next draft. The business does not have to be re-explained next week.

When the numbers room sees a problem, the growth room can use it. When a partner angle works, the content room can use it. Six rooms. One picture of the business.

## How a job enters and leaves

You run one prompt in ChatGPT, Codex, or the project you already work in. It writes `factor-harvest.md`. That file is the only handoff.

From it, Factor keeps three layers, and each has a size:

| Layer | What it is | How big |
|---|---|---|
| Instinct | Who you are, how the voice measures, what is locked | One screen, every time |
| Profile soul | The voice Hermes reads before anything else | Under 80 lines |
| Company memory | Wiki, brand, and the correction log, on disk | Open the index, then one page |

A job comes in as a sentence, a room, and the pages that match. It leaves as a draft, the pages it read, every number with the page that number came from, and a yes or no on whether you must see it.

Jev only picks and scores. It chooses the room from the list, the page from the index, and whether a person is required. It does not write the draft, and it does not invent the choices. Under half confidence, it asks. Anything that sends, spends, or publishes needs your explicit approval of the exact action and content. Confidence cannot replace that approval. When the chat gets long, Jev may drop a tool trace. It keeps the lines it keeps word for word. It does not retell them.

Claude or Codex write. You send.

## What a week looks like

You own what to build, what to publish, where to spend, and which opportunities are worth it.

The employee owns the checking, the research, and the draft.

Nothing goes out because a model finished a paragraph. It goes out because you approved it.

## Begin

```bash
git clone https://github.com/Sheshiyer/factor.git
cd factor
scripts/new-company.sh acme ~/companies/acme
```

In the project you have already been building, paste [prompts/harvest-claude.md](prompts/harvest-claude.md) into Claude, or [prompts/harvest-codex.md](prompts/harvest-codex.md) into Codex. Save `factor-harvest.md`.

```bash
scripts/onboard.py --company ~/companies/acme \
  --apply-harvest ~/src/the-project/factor-harvest.md
```

That writes the instinct, the rooms, and the business. Tools come after, and only the one the first room needs.

Then pick a door: `apps/mac/run.sh`, the Factor command in Raycast, or the `take-intent` skill in Hermes.

## Local knowledge curation

The [curation walkthrough](docs/knowledge-curation.md) imports source revisions, reviews attributed claims and replays accepted corrections in a local content packet. It preserves source gaps and conflicts, deduplicates unchanged runs and validates exact-action approval records. The [implementation plan](specs/007-knowledge-curation/plan.md) builds on the [Hermes, Grok and Jev research](docs/research/2026-09-27-agent-knowledge/README.md). These local tools do not publish or schedule work.

The [bookmark intake](docs/bookmark-ingest.md) captures a bounded FT cache selection with explicit article gaps. The [native learning guide](docs/hermes-learning-loop.md) connects reviewed work and corrections to Hermes `/learn`, pending-write review and fresh-session evaluation. The intake is locally verified; a real company/profile learning trial remains pending.

## Shipped

| Release | What it is |
|---|---|
| [v0.2.0](https://github.com/Sheshiyer/factor/releases/tag/v0.2.0) | Harvest, instinct, memory, Jev, evals, rollback |
| [v0.3.0](https://github.com/Sheshiyer/factor/releases/tag/v0.3.0) | Menu-bar tray |
| [v0.4.0](https://github.com/Sheshiyer/factor/releases/tag/v0.4.0) | Raycast and Hermes |
| [v0.5.0](https://github.com/Sheshiyer/factor/releases/tag/v0.5.0) | Rooms |

<!-- readme-gen:start:footer -->
<div align="center">



</div>
<!-- readme-gen:end:footer -->



## Source file: docs/seats.md

# Seats

Two Hermes profiles. One company repo. The menu bar, Raycast, and Hermes write an intent. They do not change the seat.

| Profile | Model | Owns |
|---|---|---|
| `factor` | Claude | The company repo, the board dispatcher, drafts, review, context updates |
| `coder` | Codex | Kanban cards whose seat is `codex`, in a worktree |

```bash
hermes profile install /absolute/path/to/factor --name factor --alias
hermes -p factor model
hermes profile create coder --no-skills \
  --description "Codex build seat. Takes Factor cards that say seat codex."
hermes -p coder model
```

`--no-skills` on `coder` keeps the bundled library from loading twice. Install the bundled `codex` skill on that profile when you want the Codex worker instructions:

```bash
hermes -p coder skills list
```

The bundled skill name is `codex`. If it is not on the profile, `hermes -p coder skills reset codex --restore` brings back a skill that shipped with Hermes.

`factor` keeps `kanban.dispatch_in_gateway: true`. Do not start a second dispatcher on `coder`.

Set the company path on the Claude profile only:

```bash
hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company
hermes -p factor config set skills.config.factor.codex_profile coder
```



## Source file: docs/doors.md

# Doors

Three doors. One intent. The door is only where you speak.

The company folder is remembered in `~/Library/Application Support/Factor/company.path`. Choose it once in the menu. Raycast and Hermes use that same path.

Each door writes `io/intent.json` with three keys: `sentence`, `room`, `door`. The card fields do not change with the door. Status is `waiting`, `ready`, or `needs you`, in `io/status.txt`.

| Door | How |
|---|---|
| Menu bar | `apps/mac/run.sh`. Unsigned and local. First launch asks for the company folder. |
| Raycast | Add `surfaces/raycast` as a script-command folder. Type the job, pick a room. |
| Hermes | The `take-intent` skill reads `io/intent.json`, then instinct, then the index, then one page, and opens one card. |

The doors do not pick a seat. Claude still writes. Codex still builds. See [seats.md](seats.md).



## Source file: docs/rooms.md

# Rooms

A new company copies these playbooks. Start with content or numbers.

| Room | File | Rule |
|---|---|---|
| Content | `desks/content/brief.md` | A short list. Each item names a page. The founder keeps, drops, or develops. The room does not publish. |
| Numbers | `desks/numbers/report.md` | Figures in one block, suggestion in another. Each figure names a page. Stay quiet when no line was crossed. |
| Partners | `desks/partners/playbook.md` | Draft the list and the briefs. Do not send them. |
| Money | `desks/money/playbook.md` | Draft the follow-up. Wait for one yes. Do not send it. |

Send, spend, and publish stay on wait in `desks/gates.md` until the founder issues an explicit approval record. Confidence alone cannot authorise a gated action; a score of 0.99 without an approval record does not send, spend, or publish.

A healthy room is quiet.



## Source file: SOUL.md

You operate one company at a time. The company is a git repo of markdown, not a pile of facts you remember.

Read `<company>/SOUL.md` before any card. It is who the owner is and how this business sounds. It was written in step 1 of onboarding, from a harvest the founder ran in Claude or Codex inside the project they were already building. The files under `context/` are the facts behind that voice.

The company root is the skill setting `factor.company_root`. If that path is empty or missing, stop and ask for it. Do not guess a directory.

Read only the files named on the card. The standing context is `context/company.md`, `context/customer.md`, `context/offer.md`, `context/positioning.md`, `context/voice.md`, and `context/proof.md`. A line that still says `FILL:` is unknown. Stop and name the file. Do not invent a price, a customer, a claim, or a result.

You are the Claude seat. You plan, draft, grade, and update a context file or a skill after a founder correction. Code goes to the Codex profile named in `docs/seats.md` of the framework, as a Kanban card with workspace `worktree`. You do not become a second coding agent.

A connector exists only when `connectors/enabled.yaml` lists it. High risk means money, people, legal, anything public, and anything paid. Those wait for an approval comment on the card. A tool that is not listed is not available, even if this machine has the token.

Instinct is `instinct.md` plus `profile-soul.md`. Instinct is one screen. The profile soul stays under 80 lines. Company memory is `wiki/`, `brand/`, and `wiki/corrections.md`. Read the index, then one page. Hermes session memory is a scratch pad. It fills quickly. Do not copy the company into it.

A job arrives as an intent from a Mac menu, Raycast, or Hermes. Name the desk, do the work, return a finished draft. Sending, spending, and publishing wait for the founder. A healthy desk stays quiet.

Save only a preference the founder just stated. Company facts go in the wiki, after the founder agrees. `AGENTS.md` stays short. A correction updates the file that was wrong, and a row in `wiki/corrections.md`.

Monday review and the quiet watch are the only standing routines. A healthy day sends nothing.



## Source file: config.yaml

# Model is chosen after install, on this profile:
#   hermes -p factor model
# Pick a Claude model here. Code work goes to a second profile whose model is Codex.
# See docs/seats.md.

kanban:
  dispatch_in_gateway: true

