<div align="center">

<img src="assets/morning.jpg" width="100%" alt="The work is finished before you sit down" />

# Factor

One employee for the work that does not need you.<br>
You keep the decisions.

</div>

<!-- readme-gen:start:badges -->
<div align="center">

![Version](https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge)
![License](https://img.shields.io/github/license/Sheshiyer/factor?style=for-the-badge)

</div>
<!-- readme-gen:end:badges -->

You already do the jobs. Content, numbers, growth, ads, partners, money. A pile of prompts made that a second job: remember the task, start it, paste the context, check the result, move it to the next tool.

Factor takes the job. You say it in plain language. The employee reads the business, does the work, and comes back with a finished draft. Research, checking, and drafting run on their own. Sending, spending, and publishing wait until you say so.

<img src="assets/doors.jpg" width="100%" alt="One intent, three doors" />

## One intent, three doors

The same employee answers from the Mac menu bar, from Raycast, and from Hermes. The door is only where you speak. The job is the same sentence wherever you are, including your phone.

| Door | What you do |
|---|---|
| Mac applet | Say the job without opening a project |
| Raycast | Say the job from the command bar |
| Hermes | Say the job from the chat you already use. It reads the intent and opens one card. |

Each door hands over one intent: the job, the room it belongs in, and the draft that comes back. Raycast and Hermes write the same file the menu bar writes.

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

A healthy room is quiet. You do not check every campaign. You see the one that changed.

<img src="assets/instinct-memory.jpg" width="100%" alt="A small instinct, and a memory that stays on the shelf" />

## Instinct, and a memory that does not fill up

Hermes remembers a little, and that little fills. Factor does not put the company there.

**Instinct** is the pocket notebook. Who the owner is, how the voice measures, and what is locked. It loads every time. It stays short.

**Memory** is the card catalog. The wiki, the brand, and the correction log live on disk. The employee reads the index, then the one page the job needs. A correction is written down as the original line, the rewrite, and the reason. The same reason twice becomes a rule. The business does not have to be re-explained next week.

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

Jev only picks and scores. It chooses the room from the list, the page from the index, and whether a person is required. It does not write the draft, and it does not invent the choices. Under half confidence, it asks. Anything that sends, spends, or publishes needs a high confidence or your yes. When the chat gets long, Jev may drop a tool trace. It keeps the lines it keeps word for word. It does not retell them.

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

The Mac applet and the Raycast command are the next doors on this same intent. Hermes is the door that already runs.

The next three releases are in [.planning/ROADMAP.md](.planning/ROADMAP.md).

<!-- readme-gen:start:footer -->
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,1&height=100&section=footer" width="100%" alt="" />

</div>
<!-- readme-gen:end:footer -->
