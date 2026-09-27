# Factor Operator Playbook

**Date:** 27 September 2026  
**Author:** Principal AI Systems Architect & Lead Technical Writer  
**Status:** Controlling Operational Guide & System Snapshot  

---

## 1. Prerequisites, Ecosystem Boundaries, and Profile Inspection

This document establishes the controlling operational truth for onboarding, configuring, and operating the Factor framework as of **27 September 2026**.

### System Scope and Conceptual Framework
The Factor ecosystem operates on a strict structural boundary explained through the **Hand, Glove, and Framework** architecture:
* **The Founder (Authority):** Retains final business authority. The founder sets direction, establishes company voice, accepts factual claims, approves procedural changes, and issues explicit authorization for gated external actions (`send`, `spend`, `publish`).
* **The Company Repository (The Glove):** An isolated Git repository (`<company>/`) containing business identity, voice guidelines, context Markdown files, wiki pages, factual claims, and correction logs.
* **The Factor Framework (Connective Logic):** Reusable operating logic, CLI scripts, onboarding templates, room contracts, and verification gates. Factor provides the connective fabric that structures work without taking ownership of company memory.
* **The Hermes Runtime (The Hand):** The execution engine that processes turns, loads procedural skills, manages local session recall, and dispatches work across dedicated profile seats.
* **Claude (`factor` profile) / Codex (`coder` profile) Seats:** Dedicated seats within Hermes. Claude handles planning, drafting, review, and context maintenance. Codex handles scoped implementation tasks on assigned Kanban cards in a workspace worktree.
* **Jev Decision Helper:** A decision boundary used strictly for selecting candidates (rooms, pages, or options) and scoring decision confidence. Jev never generates prose or writes choices.
* **Field Theory (FT):** The research capture and bookmark ingestion subsystem operating against an offline local cache.
* **NotebookLM (Documentation Synthesizer):** Used strictly as a documentation synthesis and reference compilation tool. It is **not** canonical company memory, nor is it an enabled company connector.

> [!CAUTION]
> **Controlling Negative Assertions & System Boundaries:**
> * **NO** active background schedules or automated cron routines are deployed.
> * **NO** local additions from branch `codex/factor-knowledge-curation` are pushed, merged, or deployed to remote production (committed locally at `b00dfcd`).
> * **NO** live network calls or live calibration instances are active for the Jev decision helper (validation remains fixture/shadow-based).
> * **NO** native Hermes learning pilot has been executed in a live company profile (the operational design remains pending execution).
> * **NO** authentication, identity verification, or one-time consumption is provided by local approval records (`scripts/approvals.py`), nor do they bind to an external network executor.
> * **ALL 44** repository discovery candidates inventoried during research remain completely uninstalled and disabled (0 of 44 installed).

### Status Snapshot Table

| Component | Verified System State |
| :--- | :--- |
| **Factor Framework** | Released v0.5.0 baseline. Local knowledge curation additions committed at branch commit `b00dfcd` (237 passing local unit tests, including 15 intake tests). |
| **Hermes Runtime Source** | Installed version 0.21.5 at commit `645da6561c724b7ca163d4af9c21de3a6397c9f2`. |
| **Field Theory Intake Cache** | Bounded 456-record cache (`bookmarks.jsonl`). First seven cache-order entries evaluated. Two X article bodies missing (`2099316575006240776` and `2103652547227750400`). |
| **Integrations & Execution** | 0 of 44 repository discovery candidates installed. No live Jev network calls, active schedules, or deployed execution adapters. |

### Preflight Inspection Directives
Operators must inspect existing Hermes profiles and configurations *before* running setup commands or modifying settings. Never run setup scripts blindly or execute reset/reinstall commands when profiles already exist.

Run the following inspection commands from your terminal:

```bash
# 1. List existing Hermes profiles to check for existing seats
hermes profile list

# 2. Inspect the configured company root on the 'factor' profile
hermes -p factor config get skills.config.factor.company_root
```

---

## 2. Framework Architecture, Company Setup, and Two-Seat Dispatch

### Framework vs. Company Isolation
Factor maintains absolute isolation between reusable framework logic and company-specific data. Framework code resides in the core `factor` repository checkout. Business voice, wiki documentation, context files, brand guidelines, and correction logs reside strictly inside the company Git repository (`<company>/`). Framework updates must never overwrite company facts, and company specifics must never pollute framework code.

```
<USER_HOME>/
├── factor/                    # Framework code (scripts, skills, templates)
└── companies/
    └── acme/                  # Company Repository (The Glove)
        ├── SOUL.md            # Founder voice & identity guidance
        ├── context/           # Standing facts (company, offer, customer, voice)
        ├── wiki/              # Knowledge store, claims, and corrections log
        ├── desks/             # Room work areas and playbooks
        └── output/            # Trial outputs and local run packets
```

### Initialization, Harvest, and Onboarding
To initialize a new company root, run the framework setup script:

```bash
git clone https://github.com/Sheshiyer/factor.git
cd factor
scripts/new-company.sh acme ~/companies/acme
```

Next, the founder pastes the prompt template `prompts/harvest-claude.md` (into Claude) or `prompts/harvest-codex.md` (into Codex) within their existing project workspace. The model produces a structured `factor-harvest.md` file. Apply this harvest to populate the company root:

```bash
scripts/onboard.py --company ~/companies/acme --apply-harvest ~/src/the-project/factor-harvest.md
```

This onboarding command writes three distinct operational layers into the company root:
1. **Instinct (`instinct.md`):** Loaded on every turn. Contains core owner identity, voice measurement rules, and locked boundaries. Bounded to one screen.
2. **Profile Soul (`SOUL.md` / `profile-soul.md`):** Read by Hermes before work begins. Bounded to under 80 lines.
3. **Company Memory (`wiki/`, `context/`):** Indexes and markdown context pages read on demand when a job requires specific facts.

### Two-Seat Profile Architecture
Factor operates via two dedicated Hermes profiles:
* **`factor` (Claude Seat):** Owns the company repository, dispatch logic, planning, research brief generation, drafting, review, and context maintenance.
* **`coder` (Codex Seat):** Owns execution of coding cards assigned explicitly with `seat codex` within a dedicated workspace worktree.

Install and configure the profiles using exact Hermes CLI commands:

```bash
# Install the primary factor profile
hermes profile install /absolute/path/to/factor --name factor --alias

# Create the dedicated coder profile (--no-skills prevents duplicate library loading)
hermes profile create coder --no-skills --description "Codex build seat. Takes Factor cards that say seat codex."

# Configure company root and seat linking on the factor profile ONLY
hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company
hermes -p factor config set skills.config.factor.codex_profile coder
```

### Gateway Dispatcher Configuration
In `config.yaml`, the gateway dispatcher is enabled strictly for the primary planning seat:
```yaml
kanban:
  dispatch_in_gateway: true
```

> [!WARNING]
> **Gateway Dispatcher Safety Rationale:** Do **not** set `kanban.dispatch_in_gateway: true` on the `coder` profile. Enabling the gateway dispatcher on both profiles creates concurrent polling loops that cause race conditions across worktree states during automated card processing.

---

## 3. Incremental Onboarding: Room and Capability Selection

Factor enforces a philosophy of quiet, incremental enablement. Work environments are structured into specialized "desks" (rooms). Operators must start with a single room and a single capability. Bulk installations are strictly prohibited.

### Room Architecture Summary

| Room | Desk File | Rule & Operational Boundary |
| :--- | :--- | :--- |
| **Content** | `desks/content/brief.md` | Prepares research lists and draft briefs. Items name specific pages. Founder keeps, drops, or develops. **Does not publish.** |
| **Numbers** | `desks/numbers/report.md` | Formats key figures and metric variances. Stays silent unless defined thresholds are crossed. |
| **Partners** | `desks/partners/playbook.md` | Drafts partner outreach lists and briefs. Held strictly for explicit founder sign-off; **does not send.** |
| **Money** | `desks/money/playbook.md` | Drafts invoices and payment follow-up notices. Held strictly for explicit founder sign-off; **does not send.** |

### The "Healthy Room" Rule
A healthy room is **quiet**. It operates by reading input, evaluating threshold boundaries, generating structured draft packets on disk, and stopping. A room never executes external side effects (sending messages, spending funds, publishing posts).

### Selective Capability Enablement
Capabilities from the framework catalog (`connectors/catalog.md`) must be enabled one at a time using `scripts/onboard.py`:

```bash
scripts/onboard.py --company ~/companies/acme --enable openspec
```

> [!WARNING]
> **Prohibition on Bulk Installation:** Do **not** bulk-install skills, plugins, or MCP servers. All 44 repository discovery candidates inventoried during research (e.g., Chubby Skills, BMAD, Company Brain, Bot Forge) remain disabled discovery leads.

---

## 4. Field Theory Bookmark Intake and Receipt Analysis

Field Theory (FT) bookmark ingestion operates offline via `scripts/ingest_bookmarks.py`. It converts raw JSONL bookmark caches into immutable company source revisions without invoking network requests or executing embedded code.

### Scope and Chronology Constraints
* **Scope:** Intake operates on a bounded selection (default limit: 7 records) from the local Field Theory cache (`bookmarks.jsonl`).
* **Chronology:** The selection preserves existing cache order. Because `bookmarkedAt` fields in the raw cache are `null`, cache order does **not** represent acquisition or bookmarking chronology.

### Step 1: Dry-Run Inspection
Inspect the proposed batch manifest without modifying any disk state:

```bash
python3 scripts/ingest_bookmarks.py \
  --cache /absolute/path/to/bookmarks.jsonl \
  --company /absolute/path/to/company \
  --limit 7
```

### Step 2: Applying Intake to Company
Apply the intake batch to capture post text into the company knowledge store (`wiki/knowledge.json`):

```bash
python3 scripts/ingest_bookmarks.py \
  --cache /absolute/path/to/bookmarks.jsonl \
  --company /absolute/path/to/company \
  --limit 7 \
  --apply
```

### Receipt Analysis and Missing Body Tracking
Intake generates an immutable receipt saved at `wiki/intake/bookmarks-<batch-id>.json`. The receipt enforces exact source tracking:
1. **Post Sources:** Captured under deterministic keys `ft:post:<id>`.
2. **Linked Articles:** Converted to pointer sources hashed by URL SHA-256 (`linked_page` or `x_article`).
3. **Explicit Article Gaps:** When a linked article body is absent from the cache, the importer assigns `completeness: missing` and `body: null`. 

> [!IMPORTANT]
> In current cache evidence, X articles for posts `2099316575006240776` and `2103652547227750400` remain explicitly missing (`body: null`). These gaps resulted from upstream browser session authentication limits during `ft sync`. Intake records these gaps explicitly without inventing text or failing the batch.

### Idempotency and Path Containment
* **Idempotency:** Re-running intake with identical inputs reuses existing source revisions and receipts without duplicate writes.
* **Path Safety:** Strict path guards block path traversal (`../`) and reject symbolic link escapes.

---

## 5. Knowledge Curation: Import, Review, Retrieval, and Draft Packet Boundaries

The local Python knowledge subsystem (`scripts/knowledge.py` and `scripts/content_trial.py`) governs facts, claims, and draft assembly. It operates deterministically using Python standard libraries—it does **not** invoke LLMs or generate synthetic prose.

### Source Import, Claim Lifecycle, and Human Review
To execute the curation workflow, initialize the company path and wiki index before importing source revisions, attributing claims, and conducting human reviews:

```bash
# 0. Setup disposable execution path and index target page
COMPANY_TRIAL=$(mktemp -d)/example
scripts/new-company.sh example "$COMPANY_TRIAL"
mkdir -p "$COMPANY_TRIAL/wiki"
printf '\n[Trial voice](trial-voice.md)\n' >> "$COMPANY_TRIAL/wiki/index.md"
printf '# Trial voice\nUse concrete language.\n' > "$COMPANY_TRIAL/wiki/trial-voice.md"

# 1. Import a source revision and extract the assigned revision SHA-256
SOURCE_REVISION=$(python3 scripts/knowledge.py --root "$COMPANY_TRIAL" import-source \
  --id trial-source --url https://example.test/report --author Founder \
  --body 'The product has three rooms.' --completeness complete \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["revision"])')

# 2. Add an attributed claim tied to the source revision and wiki page
python3 scripts/knowledge.py --root "$COMPANY_TRIAL" add-claim \
  --id room-count --subject product --predicate room-count \
  --statement 'The product has three rooms.' --source-id trial-source \
  --source-revision "$SOURCE_REVISION" --locator 'paragraph 1' --page trial-voice.md

# 3. Explicitly transition claim status to accepted (human review step)
python3 scripts/knowledge.py --root "$COMPANY_TRIAL" review \
  --claim-id room-count --status accepted

# 4. Retrieve verified claims for an indexed wiki page
python3 scripts/knowledge.py --root "$COMPANY_TRIAL" retrieve --page trial-voice.md
```

### Deterministic Draft Packet Assembly
`scripts/content_trial.py` acts as a deterministic packet assembler for supplied text. It verifies that claims in the text are backed by accepted claims in the knowledge store and applies accepted voice corrections.

```bash
python3 scripts/content_trial.py --root "$COMPANY_TRIAL" --page trial-voice.md \
  --card-id content-trial-1 \
  --text 'Useful product. It has three rooms. [Report](https://example.test/report)'
```

### Packet Output and Blocking Rules
The output is written as a content-addressed JSON review packet under `output/content-trials/`. 
* **Packet Structure:** Includes corrected text, accepted claims, source revision hashes, explicit gap lists, conflict lists, and mandatory fields: `local_only: true`, `published: false`, and `external_actions: []`.
* **Hard Stop Blocking Rules:** The assembly script exits with code `1` and blocks packet generation if:
  1. Any cited source body is missing or incomplete.
  2. Unreviewed, disputed, or rejected claims are present in the text.
  3. Contradictory accepted claims share the same subject/predicate.
  4. The target wiki page is unindexed or missing from `wiki/index.md`.
* **Path Failures:** Invalid inputs or path containment violations exit with code `2`.

---

## 6. Worked Example: End-to-End Research-Brief Workflow

This section walks through the first useful company job: assembling a founder-selected research brief for the content room without external publishing.

### Local Assembler vs. Live Runtime Roles
It is critical to distinguish between local Python validation and live Hermes execution:
* **Live Hermes Execution:** Claude processes the intent, reads company context, and generates the draft prose.
* **Local Assembler (`scripts/content_trial.py`):** Operates deterministically on the generated prose. It does **not** call an LLM. It enforces citation boundaries, verifies claim locators against accepted knowledge revisions, applies correction rules, and generates the immutable review packet.

### Inputs
* Founder-selected topic page in `wiki/` (e.g., `trial-voice.md`).
* 1 to 3 readable sources captured via `scripts/ingest_bookmarks.py`.
* Target desk file: `desks/content/brief.md`.

### Execution Steps
1. **Index Read:** The agent reads `wiki/index.md` and the designated context file (`context/voice.md`).
2. **Claim Retrieval:** Run `scripts/knowledge.py retrieve` against the topic page to extract accepted claims and source locators.
3. **Gap and Conflict Inspection:** Verify source completeness. Identify any missing article bodies (e.g., missing X article bodies for `2099316575006240776`) or conflicting predicate statements.
4. **Format Candidate Angles:** Construct three supported angles based strictly on accepted claims, listing explicit limitations and an abstain option.
5. **Draft Packet Assembly:** Assemble the brief packet using `scripts/content_trial.py`:
   ```bash
   python3 scripts/content_trial.py --root "$COMPANY_TRIAL" --page trial-voice.md \
     --card-id research-brief-01 \
     --text 'Research Brief Draft text with verified [Source Citation](https://example.test/report)...'
   ```

### Expected Artifact
A content review packet JSON under `output/content-trials/` containing:
* Three structured angles with verified locators.
* Corrected draft text matching the founder's measured voice.
* Source revision SHA-256 digests for all cited facts.
* Explicit non-publication flags: `"published": false`, `"external_actions": []`.

### Hard Stop Conditions
The workflow must halt immediately, log the issue, and report to the founder if:
* A cited source body is missing (`body: null`).
* A cited claim is unreviewed, disputed, or rejected.
* Contradictory accepted claims exist for the same subject/predicate.
* A path traversal attempt is detected.

---

## 7. Correction Loop: Recording, Rule Proposal, Digest Verification, and Replay

When the founder corrects draft prose, Factor captures the edit, proposes a rule upon repeated evidence, and enforces rule acceptance using exact SHA-256 page digests.

### Step 1: Recording Corrections
Log individual corrections specifying the original text, rewrite, reason, scope, and regression example:

```bash
python3 scripts/corrections.py "$COMPANY_TRIAL" record-correction \
  --original Amazing --rewrite Useful --reason 'Avoid hype' --scope trial-voice.md \
  --example 'Amazing product.'

python3 scripts/corrections.py "$COMPANY_TRIAL" record-correction \
  --original Amazing --rewrite Useful --reason 'Avoid hype' --scope trial-voice.md \
  --example 'Amazing tool.'
```

### Step 2: Proposing a Rule
When repeated evidence exists for the same reason and scope, propose a formal rule:

```bash
PROPOSAL_ID=$(python3 scripts/corrections.py "$COMPANY_TRIAL" propose-rule \
  --scope trial-voice.md --reason 'Avoid hype')
```

### Step 3: SHA-256 Digest-Guarded Acceptance
Rule acceptance requires explicit founder authorization and must be locked to the exact SHA-256 digest of the target wiki page to prevent stale updates:

```bash
# Calculate current page SHA-256 digest
PAGE_SHA256=$(python3 -c 'import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
  "$COMPANY_TRIAL/wiki/trial-voice.md")

# Accept the rule using exact digest matching
python3 scripts/corrections.py "$COMPANY_TRIAL" accept-rule \
  --proposal-id "$PROPOSAL_ID" --approver Founder --expected-sha256 "$PAGE_SHA256"
```

### Step 4: Replay and Verification
Re-run `content_trial.py` on the input draft. The trial engine replays accepted rules, automatically replacing "Amazing product." with "Useful product." while protecting Markdown links, wiki links, citations, URLs, and code spans:

```bash
python3 scripts/content_trial.py --root "$COMPANY_TRIAL" --page trial-voice.md \
  --card-id content-trial-1 \
  --text 'Amazing product. It has three rooms. [Report](https://example.test/report)'
```

> [!NOTE]
> **Mechanics of Learning:** Native Hermes `/learn` calls and Factor correction rules update local procedural files on disk (`SKILL.md`, `wiki/corrections.md`). They do **not** perform LLM fine-tuning or alter underlying model weights.

---

## 8. Future Native Hermes Learning Pilot

This operational guide specifies the configuration and execution sequence for the proposed native Hermes `/learn` pilot.

> [!IMPORTANT]
> **Pilot Status:** The native learning pilot is an audited operational design, currently **pending** execution in a real company profile. No native learning writes have been executed in live environments.

### Proposed Profile Configuration (`config.yaml`)
Configure the target Hermes profile with explicit write approval gates enabled and background review disabled for initial trial isolation:

```yaml
memory:
  write_approval: true
skills:
  write_approval: true
auxiliary:
  background_review:
    enabled: false
    max_input_tokens: 48000
```
*Rationale:* Keeping `background_review.enabled: false` initially ensures all staged skill and memory changes are directly attributable to manual `/learn` calls.

### Interactive Command Sequence
In the designated company Hermes profile chat, execute the following sequence:

```text
/learn the reviewed local Factor workflow at PATH, preserve company isolation and evidence requirements
/memory pending
/skills pending
/skills diff <ID>
/skills approve <ID>
```

### Fresh-Session Replay Validation
After approving a skill write:
1. Open a fresh, isolated session using `/new` on the gateway.
2. Re-evaluate the candidate skill on a held-out test input.
3. Confirm that the agent loads the updated skill via `skill_view` without repeating the original error.

### Verification Rule
* Pending write IDs must correspond to persisted pending disk records under `pending/` before approval.
* Approved SHA-256 skill file hashes must be verified on disk following approval.

---

## 9. Skill Ownership, Rollback, and State Management

### Ownership Boundaries
* **User-Taught Skills (`/learn`):** Foreground skills created via `/learn` are user-taught. They are **not** automatically owned by autonomous curation.
* **Curator Adoption:** Transferring a skill to autonomous curation requires explicit curator adoption (`hermes curator adopt <NAME>`).
* **Canonical Protection:** Core Factor framework skills must remain user-owned and locked against automatic background rewriting or curator modification.

### Snapshot and Rollback Protocol
Before applying system changes or skill updates, operators must follow the rollback protocol defined in `specs/006-debug-rollback/spec.md`:
1. **Pre-Snapshot Validation:** Run `scripts/check_company.py` against the target repository. A snapshot is written **only** if all company validation checks pass successfully.
2. **Directory Snapshot:** Create a clean copy of the verified company directory prior to applying changes.
3. **Execution & Verification:** Apply changes or test skill execution.
4. **Safe Rollback Execution:** If execution fails or produces regressions, restore the exact pre-application directory snapshot.

> [!WARNING]
> Attempting a rollback without a prior valid snapshot will safely halt execution and display an explicit error. Rollback never operates on an unverified or failed state snapshot.

---

## 10. Action Authorization vs. Skill Approval

A fundamental security boundary separates skill modification approvals from external action authorizations.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FOUNDER AUTHORITY BOUNDARY                       │
├───────────────────────────────────┬────────────────────────────────────┤
│     Native Hermes Skill Approval  │     Factor Action Authorization    │
│     (hermes /skills approve <ID>) │     (scripts/approvals.py)         │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Modifies skill files on disk.   │ • Authorizes external execution    │
│ • Edits procedural instructions.  │   (send, spend, publish).          │
│ • DOES NOT permit external actions│ • Binds exact payload SHA-256,     │
│   or side effects.                │   card ID, target, and expiration. │
└───────────────────────────────────┴────────────────────────────────────┘
```

### Fundamental Security Rule
Native Hermes skill approval authorizes **only** a procedural file modification on disk. It grants **zero** permission to perform gated external actions (`send`, `spend`, `publish`).

### Independent Action Approvals (`scripts/approvals.py`)
Gated actions require explicit, digest-bound human approval records generated via `scripts/approvals.py`:

```bash
# 1. Create an exact-action approval record valid for 10 minutes and capture its Approval ID
APPROVAL_EXPIRY=$(python3 -c 'from datetime import datetime,timedelta,timezone; print((datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat())')

APPROVAL_ID=$(python3 scripts/approvals.py make "$COMPANY_TRIAL" content-trial-1 publish local-review Founder \
  "$APPROVAL_EXPIRY" --payload-json '{"text":"Useful product."}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["approval_id"])')

# 2. Validate the approval record prior to any simulated action
python3 scripts/approvals.py validate "$COMPANY_TRIAL" content-trial-1 publish local-review \
  "$APPROVAL_ID" --payload-json '{"text":"Useful product."}'
```

### Payload and Confidence Rules
* **Confidence Cannot Grant Authority:** A model confidence score (even `0.99`) can **never** substitute for an explicit founder approval record.
* **Payload Invalidation:** Any change to the company root, card ID, action, target, or canonical payload JSON digest instantly invalidates the approval record.
* **Trusted-Local Boundary:** `scripts/approvals.py` provides local validation primitives only. It does not authenticate human identity, enforce one-time consumption, or interface with network transport executors.

---

## 11. Operational Troubleshooting Matrix

| Issue / Symptom | Root Cause Analysis | Verified Remediation Step |
| :--- | :--- | :--- |
| **1. Missing Article Body** | Linked source body is `null` in the intake cache (e.g., uncaptured X article due to session auth limits). | Omit the `--body` flag during import. Preserve explicit `completeness: missing` in the intake receipt. Do not invent missing text. |
| **2. Source Conflict** | Two accepted claims share a subject and predicate but contain opposing statements. | `content_trial.py` will exit code `1`. Flag the conflict for human review in `wiki/`. Keep draft creation blocked until resolved. |
| **3. Stale Page Revision** | Target wiki page SHA-256 digest changed after a correction rule was proposed. | Re-calculate current page SHA-256 digest via `hashlib`, review file diff, and re-accept the rule against the current digest. |
| **4. Missing Company Root** | `skills.config.factor.company_root` is empty or points to a non-existent path. | Set path explicitly via `hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company`. Do not guess paths. |
| **5. Unavailable Provider / Jev Timeout** | Optional ranker or LLM provider fails, times out, or returns invalid confidence. | Fall back to unpruned local context. Retain original dialogue messages word-for-word. Never counterfeit a Jev score. |
| **6. Failed Write Gates** | Hermes config unreadable or gate module import fails (`write_approval` defaults open in native tool). | Perform explicit preflight read (`hermes -p factor config get memory.write_approval`). Fix config YAML before running live sessions. |
| **7. Missing Skill Reuse** | Agent fails to execute a learned procedure in a subsequent turn. | Ensure a fresh session was started (`/new`), confirm skill write was explicitly approved, and verify skill profile scoping. |
| **8. Recurring Voice Correction** | Founder manually corrects the same prose pattern twice. | Run `corrections.py propose-rule`, obtain current page SHA-256 digest, and run `accept-rule` to lock rewrite rule into company wiki. |

---

## 12. System Progression, Operational Checklist, Metrics, and Glossary

### System Progression Path
1. **Founder Review Card:** Unified single-card interface presenting sources, explicit gaps, proposed lesson, diff, and before/after draft.
2. **Native Evaluation Receipt Bridge:** Structured receipt joining card ID, company root, native session ID, skill SHA-256 (before/after), and evaluation metrics.
3. **Proven Scheduling:** Enable automated background routines/cron **only** after repeated manual workflow successes and quiet unchanged-state verification.

### Pre-Flight Operational Checklist
Operators must complete this checklist before executing live workflows:
- [ ] Confirm company root exists and contains valid `SOUL.md` and `context/` files.
- [ ] Inspect profile settings (`hermes -p factor config get skills.config.factor.company_root`).
- [ ] Verify both write approval gates are explicitly active (`memory.write_approval=true`, `skills.write_approval=true`).
- [ ] Run dry-run bookmark intake (`scripts/ingest_bookmarks.py`) and inspect output manifest.
- [ ] Check target wiki page exists and is listed in `wiki/index.md`.
- [ ] Verify no unreviewed or conflicting claims exist for the target topic.

### Quantitative Evaluation Metrics

| Metric | Target | Measurement Method |
| :--- | :--- | :--- |
| **Unsupported Claims** | `0` | Count of factual claims in draft lacking an accepted source revision and locator. |
| **Citation Failures** | `0` | Count of broken, unindexed, or outside-root links in generated draft packets. |
| **Correction Recurrence Rate** | Declining to `0` | Frequency of repeated founder corrections for previously accepted rules. |
| **Unauthorized Action Attempts** | `0` | Any attempt to execute `send`, `spend`, or `publish` without a valid approval record. |
| **Edit Burden** | Decreasing | Character diff count between initial draft packet and final founder-accepted text. |

### Technical Glossary
* **Instinct:** Single-screen pocket notebook (`instinct.md`) loaded every turn containing core owner identity and locked rules.
* **Profile Soul:** Concise operating guidance (`SOUL.md` / `profile-soul.md`) under 80 lines read by Hermes before handling cards.
* **Company Memory:** Disk-backed index and pages (`wiki/`, `context/`, `wiki/corrections.md`) read on demand.
* **Jev:** Decision helper used exclusively to select candidates and score confidence; never generates prose.
* **Field Theory (FT):** Research capture subsystem operating against offline local JSONL bookmark caches.
* **Content Trial:** Local deterministic Python assembler (`scripts/content_trial.py`) that checks claims, replays corrections, and outputs review packets.
* **Write Approval Gate:** Native Hermes configuration key (`memory.write_approval`, `skills.write_approval`) that stages proposed writes for human review.

---

## 13. Source Map and Open Questions

### Source Map Table

| Playbook Section | Source Reference Path |
| :--- | :--- |
| **Ecosystem Status & Scope** | `00-current-truth.md`, `01-factor-architecture.md` |
| **Architecture & Seats** | `docs/seats.md`, `docs/doors.md`, `SOUL.md`, `config.yaml` |
| **Curation & Intake CLI** | `docs/knowledge-curation.md`, `docs/bookmark-ingest.md`, `specs/007-knowledge-curation/spec.md` |
| **Native Learning Loop** | `docs/hermes-learning-loop.md`, `prompts/hermes-learn-reviewed-workflow.md` |
| **Audit & Capability Matrix** | `docs/research/2026-09-27-latest-seven/hermes-native-audit.md` |
| **Verification & Tests** | `specs/007-knowledge-curation/verification.md`, `specs/008-native-learning/verification.md` |

### Open Operational Questions
1. Retrieval and ingestion of missing article bodies for X posts `2099316575006240776` and `2103652547227750400`.
2. Execution of the first live native Hermes `/learn` pilot in an explicit, isolated company profile.
3. Implementation of the unified Founder Review Card and native evaluation receipt schema bridge.
4. Authenticated multi-user human identification and executor binding for `scripts/approvals.py`.