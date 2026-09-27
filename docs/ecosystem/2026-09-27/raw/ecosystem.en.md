# Factor Ecosystem Guide

### Document Metadata
* **Document Title:** Factor Ecosystem Guide
* **Date:** 27 September 2026
* **Documentation Synthesis Tool:** NotebookLM (explicitly noted as a documentation synthesis tool, not canonical company memory or an enabled company connector).

---

## 1. Purpose & Ecosystem Status Matrix

### 1.1 Objective & Controlling Truth
The primary purpose of the Factor ecosystem is to provide an operating framework that delivers reusable procedures, structured execution environments, and automated administrative support for autonomous work while rigorously preserving human agency. Factor executes routine drafting, research, code synthesis, and data compilation tasks, but reserves final authorization, strategic intent, and consequential decision-making exclusively for the human founder. The system enforces an architecture where confidence scores never substitute for explicit human authorization.

The single controlling status snapshot for the ecosystem is established in `00-current-truth.md`. All operational claims, capability evaluations, and system configurations are governed by a strict hierarchy of source precedence:

> **Source Precedence Rule:**  
> Dated Verification & Native Audits > Current Operating Guides > Design Specs > Promotional READMEs

A design spec or code example in documentation does not constitute a deployed or verified runtime result. Implementation claims are valid only when backed by passing local verification suites, executed receipts, or direct native source code audits.

### 1.2 Ecosystem Status Matrix
The following matrix summarizes the verified state of all ecosystem system tiers as of 27 September 2026:

| Tier / Component | Version / Commit Identifier | Current Verification State | Status Classification | Key Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **Factor Framework Baseline** | Released v0.5.0 (`795ae67`) | Fully verified; 58 original GitHub issues closed and reconciled across R1–R3 milestones in `.planning/GITHUB-RECONCILIATION.md`. | Released | Baseline foundation for harvest, instinct, memory, Jev, evals, and room playbooks. |
| **Local Curation Additions** | Branch `codex/factor-knowledge-curation` (through `b00dfcd`) | Verified locally; 237 standard library tests passing in 5.285 seconds. | Local Addition | Unpushed, unmerged, and undeployed to remote branches or live servers. |
| **Hermes Runtime Source** | Installed version `0.21.5` (`645da6561c724b7ca163d4af9c21de3a6397c9f2`) | Source-audited against upstream main (`806fa64f`, 3181 commits ahead). | Installed Source | Upstream main removed hardcoded semver; do not update runtime purely based on semver. Effective profile settings uninspected. |
| **Field Theory (FT) Ingestion** | Local cache scan (456 records); selected batch is first 7 records | Verified offline dry-run and apply to disposable target; 12 total sources captured (7 post bodies + 5 linked page pointers; 2 X article bodies missing). | Local Cache Scan | Save chronology unknown (`bookmarkedAt` is null). 45 shortlinks resolved to 44 repo destinations (0 installed). |
| **Jev Decision Helper** | Local shadow/fixture validation (`scripts/jev_decisions.py`) | Shadow/fixture validation complete; typed candidate membership verified. | Local Shadow / Fixture | Zero live provider API calls or live quality claims. |
| **Native Learning Loop** | Source-verified operating design (`docs/hermes-learning-loop.md`) | Verified against Hermes native capabilities (`/learn`, pending writes). | Proposed Pilot | Live profile runtime pilot *pending* (unexecuted). No model-weight training implied. |

> **PROHIBITED CLAIMS & BOUNDARIES**  
> System operators and synthetic documentation synthesis tools are strictly forbidden from claiming: active execution schedules, deployed local branch changes, live Jev API provider calls, completed native learning pilots, authenticated one-time approval consumption, or that any of the 44 inventoried candidate repositories are installed.

---

## 2. System Metaphor & Human Authority Boundaries

### 2.1 The Hand, the Glove, and the Framework
The Factor ecosystem divides responsibilities across four distinct entities to prevent authority leakage and isolate execution state from company facts:

* **The Hand (Hermes Runtime):** The active execution engine. It carries the agent across conversational turns, executes tool calls, manages profile-local scratchpad memories, and stages procedural skills. The hand is completely decoupled from company identity.
* **The Glove (Company Repository):** A fitted external Git directory owned by the founder. It holds company-specific voice instructions (`SOUL.md`), standing facts (`context/`), structured memory (`wiki/`), historical corrections (`wiki/corrections.md`), and explicit authorization records (`approvals/`).
* **The Framework (Factor):** The reusable operating structure. It supplies blank company templates (`company/`), room contracts, onboarding scripts, validation tools, and cross-door intent schemas that connect the hand to the glove without polluting the runtime with proprietary facts.
* **The Founder:** The ultimate authority. The founder establishes strategic direction, defines company tone, corrects operational errors, and holds non-delegable gating power over all consequential actions.

```
+-----------------------------------------------------------------------------------+
|                                    THE FOUNDER                                    |
|             (Holds Strategic Intent, Voice Rules, & Absolute Authority)           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            THE FRAMEWORK (Factor v0.5.0)                          |
|         (Reusable Playbooks, Room Contracts, Door Schemas, Validation Scripts)     |
+-----------------------------------------------------------------------------------+
                       /                                     \
                      v                                       v
+------------------------------------------+ +--------------------------------------+
|           THE HAND (Hermes 0.21.5)       | |      THE GLOVE (Company Repository) |
|  - Active Execution Engine               | |  - Voice (SOUL.md, instinct.md)       |
|  - Profile Scratchpad & Session Recall   | |  - Standing Facts (context/)        |
|  - Tool Dispatch & Skill Staging         | |  - Knowledge & Rules (wiki/)       |
+------------------------------------------+ +--------------------------------------+
```

### 2.2 Non-Negotiable Human Authority Rules
High-risk operations are strictly defined as any action involving money, public communications, legal commitments, financial spending, or content publishing. High-risk actions remain permanently gated in `desks/gates.md` and cannot be executed autonomously.

* **Confidence is Not Permission:** Model confidence scores and Jev decision ratings are internal heuristics, not authorization primitives. A Jev or LLM confidence score of `0.99` can never bypass human approval.
* **Local Approval Primitive Contract:** As implemented in `scripts/approvals.py`, a valid approval record requires an explicit JSON object bound to seven parameters:
  1. Company Root Path
  2. Card ID
  3. Action Identifier (e.g., `publish`, `send`, `spend`)
  4. Target Resource
  5. Canonical Payload SHA-256 Digest
  6. Approver String Identifier
  7. Expiration ISO Timestamp
* **Validation Scope:** Any modification to the underlying payload, action scope, target, or card ID immediately invalidates the approval record. Local approval files validate structural schema and payload integrity; they do not authenticate human identity, supply cryptographic signatures, or provide external network transport.
* **Jev Shadow & Context Compaction Rules:** When Jev context ranking fails or times out, the system retains all original messages verbatim. Compaction algorithm rules strictly enforce the preservation of protected prohibitions, commitments, paths, and unresolved questions without dropping or rewriting them.

---

## 3. Component Ownership & Responsibility Matrix

| Component | Primary Responsibility | Data Storage Location | Authority Limit / Constraints |
| :--- | :--- | :--- | :--- |
| **Factor Framework** | Reusable playbooks, room definitions, catalog cards, onboarding templates, CLI validation scripts. | Local repo checkout (`scripts/`, `desks/`, `catalog/`) | Blueprint provider only; holds zero state, business facts, or credentials. |
| **Company Repository** | Canonical business identity, standing facts, wiki index, voice rules, corrections, local approval records. | External Git folder (`companies/<name>/`) | Single-writer local file boundary; no direct execution capabilities. |
| **Hermes Runtime** | Multi-turn execution, tool invocation, session persistence, profile scratchpads, native skill staging. | `~/.hermes/profiles/<profile>/` | Operates strictly as execution engine; cannot alter gated company policy. |
| **Claude Seat (`factor` profile)** | Intent processing, board dispatching, drafting, wiki maintenance, contextual updates, review preparation. | Configured via `skills.config.factor.company_root` | `kanban.dispatch_in_gateway: true`; delegates code tasks, cannot publish autonomously. |
| **Codex Seat (`coder` profile)** | Technical implementation and code modification cards assigned explicitly to `seat: codex`. | Isolated Git worktrees (`workspace worktree`) | Installed with `--no-skills` to prevent duplicate library loading; no gateway dispatch. |
| **Field Theory (FT)** | Source discovery, external post/bookmark caching, pointer resolution. | Local JSONL cache (`bookmarks.jsonl`) | Passive intake cache; cannot execute commands, accept claims, or alter company wiki. |
| **Jev Helper** | Bounded room/page ranking, candidate selection, confidence scoring. | Local shadow scripts (`scripts/jev_decisions.py`) | Bounded candidate selection only; prohibited from drafting prose or inventing choices. |
| **NotebookLM** | Offline synthesis, cross-source analysis, documentation generation. | Synthetic execution context | Documentation synthesis tool only; explicitly NOT canonical memory or a live connector. |

---

## 4. Entry Architecture: Three Doors, One Intent, and Dual Seats

```
         +-----------------------------------------------------------------+
         |                          FOUNDER INTENT                         |
         +-----------------------------------------------------------------+
                                          |
          +-------------------------------+-------------------------------+
          |                               |                               |
          v                               v                               v
   [ Menu Bar Door ]              [ Raycast Door ]               [ Hermes Door ]
  (apps/mac/run.sh)             (surfaces/raycast)            (take-intent skill)
          |                               |                               |
          +-------------------------------+-------------------------------+
                                          |
                                          v
                         +---------------------------------+
                         |        io/intent.json           |
                         |  { sentence, room, door }       |
                         +---------------------------------+
                                          |
                                          v
                         +---------------------------------+
                         |        io/status.txt            |
                         |  (waiting | ready | needs you)  |
                         +---------------------------------+
                                          |
                                          v
                         +---------------------------------+
                         |      Factor Kanban Card         |
                         +---------------------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
        [ Claude Seat: factor ]                       [ Codex Seat: coder ]
       (Planning, Drafts, Wiki)                     (Code Worktree Cards)
```

### 4.1 The Three Doors & Intent Standardization
Access to the Factor ecosystem is provided through three entry points ("doors"). The door determines only the interface through which the founder speaks; it does not alter execution rules or seat assignments.

1. **Mac Menu Bar (`apps/mac/run.sh`):** An unsigned, local macOS tray application allowing quick entry without opening a terminal or IDE. Prompts for the active company path on first launch.
2. **Raycast Extension (`surfaces/raycast`):** A command-bar extension enabling rapid task dispatch directly from the Raycast launcher interface.
3. **Hermes Chat Door:** Natural language interaction within an active Hermes chat session, utilizing the bundled `take-intent` skill.

**Intent Standardization:**  
Regardless of the door utilized, all entry points read the target company path stored in `~/Library/Application Support/Factor/company.path` and write an identical JSON structure to `io/intent.json`. The payload is strictly constrained to three keys:

```json
{
  "sentence": "Draft a brief on recent AI agent research.",
  "room": "content",
  "door": "raycast"
}
```

This intent file is converted into a standard Factor Kanban card. Operational status is tracked asynchronously via `io/status.txt`, containing explicit values: `waiting`, `ready`, or `needs you`.

### 4.2 The Dual-Seat Execution Model
Factor decouples general reasoning and strategy from technical code execution by establishing two segregated Hermes profiles (`docs/seats.md`):

* **Profile `factor` (Claude Model):**
  * **Configuration:** Configured with `hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company` and linked to the Codex seat via `hermes -p factor config set skills.config.factor.codex_profile coder`. Maintains `kanban.dispatch_in_gateway: true`.
  * **Responsibilities:** Board dispatching, context updates, content drafting, weekly reviews, and wiki updates.
* **Profile `coder` (Codex Model):**
  * **Configuration:** Installed using `hermes profile create coder --no-skills` to prevent duplicate skill loading.
  * **Responsibilities:** Evaluates Kanban cards marked specifically with `seat: codex`. Performs engineering work in isolated Git worktrees. Does not run a gateway dispatcher or act as a primary interface.

```bash
# Setup commands for dual-seat execution model
hermes profile install /absolute/path/to/factor --name factor --alias
hermes profile create coder --no-skills \
  --description "Codex build seat. Takes Factor cards that say seat codex."

hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company
hermes -p factor config set skills.config.factor.codex_profile coder
```

---

## 5. Operational Scopes: The Six Rooms

### 5.1 Room Definitions & Automated vs. Quiet Realities
Factor organizes operational tasks into six functional rooms. A primary core design principle governs all rooms: **"A healthy room is quiet."** Systems do not execute continuous polling to generate noise; they report only when explicitly triggered, when thresholds are crossed, or when a human decision is required.

| Room | Playbook / File | Purpose & Output Contract | Desired Cadence | Current Automation Reality |
| :--- | :--- | :--- | :--- | :--- |
| **Content** | `desks/content/brief.md` | Researched brief with page citations. Founder keeps, drops, or develops. | Daily / Weekdays | Manual CLI trigger (`content_trial.py`); deterministic packet assembler. No LLM generation or publishing. |
| **Numbers** | `desks/numbers/report.md` | Key metrics block with cross-referenced page citations. | Periodic / Weekly | Silent unless predefined metric threshold is crossed. Local file integrity checks only. |
| **Growth** | `desks/growth/playbook.md` | Short list of strategic build opportunities supported by evidence. | Weekly | Draft preparation only. No external acquisition or active web scraping. |
| **Ads** | `desks/ads/playbook.md` | Proposed campaign modifications crossing set budget/performance lines. | Exception-based | Draft preparation only. Ad spend or network transmission strictly gated. |
| **Partners** | `desks/partners/playbook.md` | Vetted partner lists and outreach briefs. | Periodic | Prepares drafts; wait state enforced in `desks/gates.md`. No message sending. |
| **Money** | `desks/money/playbook.md` | Invoice drafts and weekly financial summaries. | Weekly | Drafts wait for explicit founder "yes". Zero live banking or payment API calls. |

---

## 6. Company Repository Information Architecture

### 6.1 Directory Anatomy & File Rules
A standardized company repository (`companies/<name>/`) separates short-term execution instructions from long-term memory:

```
companies/<name>/
├── SOUL.md                  # Owner identity & voice rules (derived step 1)
├── instinct.md              # Pocket notebook (always loaded, 1 screen max)
├── profile-soul.md          # Hermes soul prefix (under 80 lines)
├── context/                 # Standing facts (FILL: lines retain unknown state)
│   ├── company.md
│   ├── customer.md
│   ├── offer.md
│   ├── positioning.md
│   ├── voice.md
│   └── proof.md
├── wiki/                    # Disk-based card catalog
│   ├── index.md             # Primary index file
│   ├── corrections.md       # Log of historical corrections
│   └── synthesis/           # Cross-source conclusions
└── approvals/               # Local action approval records
```

* **Memory Budget Rules:**
  * `instinct.md`: Always loaded into context. **Budget:** Must fit entirely on one screen.
  * `profile-soul.md`: Hermes-specific soul prefix. **Budget:** Strictly under 80 lines.
  * `context/`: Standing facts. Unfilled template lines retain explicit `FILL:` markers. LLMs are prohibited from inventing facts or filling empty markers without evidence.
  * `wiki/`: Primary memory store accessed on-demand by reading `wiki/index.md` first, then opening only the specific required page.

### 6.2 Correction Promotion & Rule Lifecycle
When a draft evaluation fails, Factor executes a 5-step deterministic propagation sequence:

```
[Founder Identifies Draft Error]
               │
               ▼
[1. Record Row in wiki/corrections.md]
  - Original Text
  - Founder Rewrite
  - Reason
  - Page Scope
               │
               ▼
[2. System Detects 2 Matching Reasons]
  - Generates Proposed Rule
               │
               ▼
[3. Founder Reviews & Accepts Rule]
  - Accepts against exact page SHA-256 digest via scripts/corrections.py
               │
               ▼
[4. Replay & Apply to Subsequent Drafts]
  - Re-evaluates accepted rules against new text
  - Protects links, code spans, & citations
               │
               ▼
[5. Procedural Adaptation]
  - Updates procedural files (skills/pages)
  - Zero modification to underlying model weights
```

#### Deterministic Lifecycle Execution
1. **Record Correction:** The founder records a row in `wiki/corrections.md` containing `original`, `rewrite`, `reason`, `scope`, and `example` via `python3 scripts/corrections.py "$COMPANY_DIR" record-correction`.
2. **Rule Proposal:** Upon logging two matching reasons for the same scope, `python3 scripts/corrections.py "$COMPANY_DIR" propose-rule` generates a page-scoped rule proposal.
3. **Human Acceptance:** The founder accepts the rule against the exact reviewed page SHA-256 digest via `python3 scripts/corrections.py "$COMPANY_DIR" accept-rule`.
4. **Draft Replay:** Subsequent assembly via `python3 scripts/content_trial.py` re-evaluates accepted rules against new text while preserving Markdown links, reference citations, code spans, and URLs.
5. **Procedural Adaptation:** Learned corrections modify disk-based instructions and procedural files; they never imply model-weight fine-tuning.

```bash
# Detailed CLI correction lifecycle walkthrough
python3 scripts/corrections.py "$COMPANY_TRIAL" record-correction \
  --original Amazing --rewrite Useful --reason 'Avoid hype' --scope trial-voice.md \
  --example 'Amazing product.'

python3 scripts/corrections.py "$COMPANY_TRIAL" record-correction \
  --original Amazing --rewrite Useful --reason 'Avoid hype' --scope trial-voice.md \
  --example 'Amazing tool.'

PROPOSAL_ID=$(python3 scripts/corrections.py "$COMPANY_TRIAL" propose-rule \
  --scope trial-voice.md --reason 'Avoid hype')

PAGE_SHA256=$(python3 -c 'import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
  "$COMPANY_TRIAL/wiki/trial-voice.md")

python3 scripts/corrections.py "$COMPANY_TRIAL" accept-rule \
  --proposal-id "$PROPOSAL_ID" --approver Founder --expected-sha256 "$PAGE_SHA256"

python3 scripts/content_trial.py --root "$COMPANY_TRIAL" --page trial-voice.md \
  --card-id content-trial-1 \
  --text 'Amazing product. It has three rooms. [Report](https://example.test/report)'
```

---

## 7. Capability Catalog Selection Lifecycle

Factor isolates external tool integration across five strict lifecycle stages:

1. **Offered:** Capability definitions available in `catalog/cards/` or `connectors/registry.yaml`, derived from ecosystem inventory scans.
2. **Selected:** Explicitly chosen by the founder during onboarding (`scripts/onboard.py --enable <id>`) or configured in `connectors/enabled.yaml`.
3. **Installed:** Assets deployed to the profile via `hermes profile install` or MCP definitions registered in `~/.hermes/profiles/factor/`.
4. **Configured:** Environment variables defined in `~/.hermes/profiles/factor/.env` and tool allowlists locked down using `hermes mcp configure <name>`.
5. **Verified:** Integrations tested locally with recorded execution receipts proving compliance.

> **Inventory vs. Installation Boundary:**  
> During the Field Theory bookmark audit, 44 candidate repository destinations were cataloged as *Offered* discovery leads. **Zero (0)** of these repositories are currently installed or enabled within the runtime.

---

## 8. Knowledge Curation Lifecycle & Local Primitives

### 8.1 The Local Knowledge Pipeline
The knowledge curation pipeline (`scripts/knowledge.py`, `scripts/content_trial.py`) operates entirely using Python standard library primitives, producing local files without making LLM calls or network requests. The local JSONL cache is strictly bounded to 64 MiB, and lines are split strictly on LF while preserving Unicode line separators (`U+2028`/`U+2029`) inside post bodies.

```
+-----------------------------------------------------------------------------------+
| 1. IMPORT SOURCE (knowledge.py import-source)                                    |
|    - Assigns Source ID (ft:post:<id> or URL SHA-256)                              |
|    - Computes Immutable SHA-256 Content Revision Digest                           |
|    - Missing bodies recorded explicitly as completeness: missing                  |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 2. ADD CLAIM (knowledge.py add-claim)                                             |
|    - Binds statement to Source ID, Revision SHA-256, Locator, and Wiki Page       |
|    - Initial Status: CAPTURED                                                     |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 3. HUMAN REVIEW (knowledge.py review)                                             |
|    - Human updates status to ACCEPTED, DISPUTED, or REJECTED                      |
|    - Only ACCEPTED claims are eligible for retrieval                              |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 4. RETRIEVAL & ASSEMBLY (knowledge.py retrieve / content_trial.py)               |
|    - Queries indexed wiki pages (wiki/index.md)                                   |
|    - Surfaces accepted claims; flags gaps & conflicting accepted predicates       |
|    - Outputs JSON Review Packet under output/content-trials/                      |
|    - Exit Code 1: Blocked packet (gaps or conflicting claims)                     |
|    - Exit Code 2: Invalid input or path containment failure                       |
+-----------------------------------------------------------------------------------+
```

#### Executable Command Sequence
```bash
# 1. Import Source Body
SOURCE_REVISION=$(python3 scripts/knowledge.py --root "$COMPANY_DIR" import-source \
  --id trial-source --url https://example.test/report --author Founder \
  --body 'The product has three rooms.' --completeness complete \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["revision"])')

# 2. Bind Claim to Source Revision
python3 scripts/knowledge.py --root "$COMPANY_DIR" add-claim \
  --id room-count --subject product --predicate room-count \
  --statement 'The product has three rooms.' --source-id trial-source \
  --source-revision "$SOURCE_REVISION" --locator 'paragraph 1' --page trial-voice.md

# 3. Explicit Human Review
python3 scripts/knowledge.py --root "$COMPANY_DIR" review \
  --claim-id room-count --status accepted

# 4. Query & Retrieve Indexed Claims
python3 scripts/knowledge.py --root "$COMPANY_DIR" retrieve --page trial-voice.md

# 5. Assemble Local Content Packet
python3 scripts/content_trial.py --root "$COMPANY_DIR" --page trial-voice.md \
  --card-id content-trial-1 \
  --text 'Amazing product. It has three rooms. [Report](https://example.test/report)'
```

#### Programmatic Exit Codes
* **Exit Code 0:** Execution succeeded; content packet assembled with all claims accepted.
* **Exit Code 1:** Execution produced a blocked packet due to missing sources, unaccepted claim gaps, or conflicting accepted predicates.
* **Exit Code 2:** Script execution failed due to invalid input arguments, malformed JSON payloads, or path containment/symlink escape violations.

### 8.2 Missing Sources & Synthesis Rules
During the 27 September 2026 Field Theory intake dry-run scan, 12 total sources were captured. These 12 sources consist of **7 primary post bodies** plus **5 linked page pointers**. Two X article bodies remain missing/unretrieved:
* `coldemailchris` article (`2099316575006240776`)
* `DhravyaShah` article (`2103652547227750400`)

**Synthesis Rules:** Primary repository reviews (such as the Company Brain primary repository audit) supplement ecosystem understanding but do *not* substitute for missing article bodies. Unfetched source text is explicitly recorded with `completeness: missing`. Extracted research data remains non-canonical context until explicitly reviewed and accepted by the founder.

---

## 9. Native Learning Loop, Ownership, & Fail-Open Guardrails

### 9.1 The Factor + Hermes Learning Loop
Factor leverages native Hermes runtime capabilities (installed source `0.21.5` at commit `645da656`) for procedural adaptation, avoiding external background learning daemons.

```
+-----------------------------------------------------------------------------------+
| 1. EXECUTE BASELINE                                                               |
|    Run task; record raw evidence, output, time, and human edit burden.            |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 2. CLASSIFY FEEDBACK                                                              |
|    - Factual Error    ──> Wiki / Claim Update                                     |
|    - Voice Error      ──> wiki/corrections.md                                     |
|    - Procedural Defect──> Native Skill Candidate                                  |
|    - Small Preference ──> Profile-Local Memory                                    |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 3. DISTILL PROCEDURE                                                              |
|    Invoke native /learn using prompts/hermes-learn-reviewed-workflow.md.          |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 4. REVIEW STAGED WRITES                                                           |
|    Inspect pending writes: /skills pending, /skills diff ID, /memory pending.     |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 5. FRESH SESSION REPLAY                                                           |
|    Open clean session (/new); re-test procedure on held-out input fixture.        |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| 6. DISPOSITION                                                                    |
|    Mark candidate as KEEP, REVISE, or RETIRE based on objective evaluation metrics|
+-----------------------------------------------------------------------------------+
```

### 9.2 Critical Native Security & Fail-Open Caveats
Source code audits (`hermes-native-audit.md`) revealed critical security findings regarding native write gates:

* **Fail-Open Behavior in Write Gates:** In `tools/write_approval.py:43-59` and `tools/skill_manager_tool.py:627-636`, unreadable or malformed gate configuration files, or a gate module import failure, cause native write gates to **fail open** (gates disabled).
* **Fail-Open Behavior in Memory Tool:** In `tools/memory_tool.py:84-91`, if importing the write-approval module fails, the system bypasses write approval checks and allows normal memory writes.
* **Background Memory Unattended Edits:** In `tools/memory_tool.py:164-190`, the unattended replace/remove guard stages destructive background memory edits even when the general memory write gate is disabled.
* **Mandatory Gate Verification:** System administrators must explicitly inspect runtime gate state using CLI commands (`hermes -p factor config get memory.write_approval`) rather than assuming static YAML files enforce security bounds.
* **Staging Limitations:** A returned pending write ID indicates staged metadata in memory; it does not guarantee verified disk write persistence (`tools/write_approval.py:75-92`). Native skill approval replays file-writing operations but lacks SHA-256 page-digest compare-and-swap validation.
* **Ownership Boundaries:** User-taught foreground `/learn` skills remain strictly user-owned (`tools/skill_manager_guards.py:180-232`). Autonomous curation daemons cannot edit or adopt user-owned skills unless `hermes curator adopt <name>` is explicitly executed.

### 9.3 Proposed Pilot Configuration (Unexecuted)
The following profile configuration represents a proposed pilot setup for runtime validation. It is explicitly tagged as **UNEXECUTED**:

```yaml
# PROPOSED RUNTIME PILOT CONFIGURATION (UNEXECUTED)
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: true      # Proposed: Require explicit approval for memory writes
  nudge_interval: 10
skills:
  write_approval: true      # Proposed: Require explicit approval for skill edits
  creation_nudge_interval: 10
auxiliary:
  background_review:
    enabled: false          # Proposed: Keep false during initial manual trial
    max_input_tokens: 48000
    extra_tools: []
```

---

## 10. Practical Use Cases & Operational Workflows

### 10.1 Primary Use Cases

#### 1. Research-to-Content Brief
* **Inputs:** Founder-selected topic, 1–3 readable source revisions.
* **Process:** Extract attributed claims $\rightarrow$ highlight gaps and contradictions $\rightarrow$ draft 3 candidate angles $\rightarrow$ founder selects outline $\rightarrow$ generate cited draft.
* **Feedback:** Record edits in `wiki/corrections.md`; promote repeated edits to page rules.

#### 2. Founder Knowledge Answer
* **Process:** Retrieve indexed pages from `wiki/index.md` $\rightarrow$ match accepted claims $\rightarrow$ construct concise response with explicit source locators $\rightarrow$ explicitly output `"UNKNOWN"` for unindexed or missing details.

#### 3. Implementation Companion
* **Process:** Read assigned card $\rightarrow$ generate narrow specification and domain model $\rightarrow$ delegate code modifications to Codex seat (`coder` profile) operating in a dedicated Git worktree $\rightarrow$ execute local test suite (`python3 -m unittest`).

### 10.2 Deferred Candidate Scopes

> **DEFERRED / NON-DEPENDENCY CANDIDATES**  
> The following operational scopes are categorized as deferred candidate integrations. None represent active dependencies or installed components:
> 1. **Competitor-Change Watcher:** Passive monitoring deferred until quiet-state filtering is proven.
> 2. **Public-Asset OSINT Inventory:** Asset discovery (SpiderFoot/theHarvester concepts) deferred pending target authorization contracts.
> 3. **Video Production Pipeline:** Multi-stage rendering pipeline (ViMax concept) deferred pending asset rights and provider credential setup.

---

## 11. Local Verification, Commit Baselines, & Boundaries

### 11.1 Test Suite & Verification Records
System integrity is validated using standard library test suites (`unittest`):

* **Baseline Release (v0.5.0):** 30 core tests passing.
* **Phase 007 Baseline (Knowledge Curation):** 222 tests passing.
* **Phase 008 Baseline (Bookmark Intake & Native Design):** **237 tests passing** (execution time: 5.285 seconds, exit code 0).

```
======================================================================
Verification Test Suite Coverage:
 - Source Import & Immutable SHA-256 Content Addressing
 - Idempotent Intake & Duplicate Rejection
 - Path Traversal & Symlink Escapes Rejection
 - Exact-Action Local Approval Record Validation
 - Jev Shadow Decision & Context Compaction Validation
 - Field Theory JSONL Cache Parsing & Gap Accounting
======================================================================
237 tests passed in 5.285s (OK)
```

**Jev Shadow Compaction Behavior:** Verification confirms that when Jev ranking fails, the system retains all original messages verbatim. Compaction preserves protected prohibitions, commitments, paths, and unresolved questions without dropping or rewriting them.

### 11.2 Trust Boundaries & Environment Isolation
* **Single-Writer Model:** Storage mechanisms assume a trusted single-operator execution model. They do not implement multi-tenant sandboxing or concurrent multi-user locking.
* **Approver String Identity:** Approver values stored in approval records are plain string identifiers, not cryptographically signed public-key identity assertions.
* **Path Masking:** Environment logs and error traces must mask absolute personal machine directories using `<USER_HOME>` or repo-relative paths.

---

## 12. Implementation Progression, Source Map, & Open Questions

### 12.1 Phase Connection & Historical Reconciliation
* **GitHub Historical Reconciliation:** The original GitHub planning board (58 items across milestones R1–R3) was fully closed and reconciled in `.planning/GITHUB-RECONCILIATION.md`. Remaining open milestone containers represent remote GitHub metadata lag, not incomplete code.
* **Phase 007 Implementation:** Established local standard library curation tools (`knowledge.py`, `corrections.py`, `approvals.py`, `content_trial.py`).
* **Phase 008 Implementation:** Added bounded Field Theory intake (`ingest_bookmarks.py`), Hermes source audit, and native learning design.
* **Superseding Precedence Rule:** Historical specification wording from R1–R3 is explicitly superseded by Phase 007/008 verified test states. Historical aspirations must never be cited as current release realities.

### 12.2 System Glossary
* **The Hand:** The active Hermes execution engine carrying the agent across turns, executing tool calls, and managing local profile state. Decoupled from company identity.
* **The Glove:** The fitted external Git company repository containing voice rules (`SOUL.md`), standing facts (`context/`), memory (`wiki/`), and corrections (`wiki/corrections.md`).
* **Instinct:** The pocket notebook file (`instinct.md`) loaded into context on every turn, strictly budgeted to fit on a single screen (max 1 screen).
* **Profile Soul:** The Hermes-specific voice instruction file (`profile-soul.md`) loaded before turn execution, strictly budgeted under 80 lines.
* **Jev:** The decision helper bounded to selecting/ranking supplied candidate IDs; prohibited from drafting prose or generating choices outside explicit lists.
* **Door:** An entry interface (Mac Menu Bar, Raycast Extension, or Hermes Chat) that standardizes user requests into an identical `io/intent.json` schema (`sentence`, `room`, `door`).
* **Room:** An operational domain playbook operating under quiet-state rules (reports only when explicit thresholds are crossed or action is required).
* **Content Trial:** The local CLI assembler (`scripts/content_trial.py`) that constructs cited JSON review packets using Python standard library primitives without LLM invocation. Exit code 1 indicates blocked gaps/conflicts; exit code 2 indicates path/input errors.
* **Approval Record:** A local JSON file created via `scripts/approvals.py` binding 7 canonical parameters: company root, card ID, action, target, canonical payload SHA-256 digest, approver string, and expiration timestamp.
* **Native Skill:** A procedural `SKILL.md` file managed by native Hermes skill tools (`/learn`, `skill_manage`), stored locally within profile directories under user-taught ownership.

### 12.3 Traceable Source Map

| Document Section | Primary Controlling Source File | Key Relative Paths / References |
| :--- | :--- | :--- |
| **Ecosystem Truth & Matrix** | `00-current-truth.md` | `.planning/STATE.md`, `.planning/GITHUB-RECONCILIATION.md` |
| **Architecture & Metaphor** | `01-factor-architecture.md` | `README.md`, `SOUL.md` |
| **Doors & Seats** | `01-factor-architecture.md` | `docs/doors.md`, `docs/seats.md` |
| **Six Rooms & Cadence** | `01-factor-architecture.md` | `docs/rooms.md`, `desks/gates.md` |
| **Curation & Local Primitives** | `02-knowledge-and-intake.md` | `docs/knowledge-curation.md`, `scripts/knowledge.py` |
| **Bookmark Intake** | `02-knowledge-and-intake.md` | `docs/bookmark-ingest.md`, `scripts/ingest_bookmarks.py` |
| **Native Learning & Audit** | `03-native-learning.md` | `docs/hermes-learning-loop.md`, `hermes-native-audit.md` |
| **Verification & Specs** | `04-implementation-and-evidence.md` | `specs/007-knowledge-curation/`, `specs/008-native-learning/` |
| **Research & Candidates** | `05-research-and-use-cases.md` | `docs/research/2026-09-27-agent-knowledge/` |
| **Memory & Jev Contracts** | `06-design-contracts.md` | `specs/002-memory/`, `specs/003-jev/`, `connectors/catalog.md` |

### 12.4 Open Questions & Next Steps
1. **X Article Body Retrieval:** How will missing article bodies for `2099316575006240776` and `2103652547227750400` be authenticated and fetched?
2. **Live Pilot Execution:** Provisioning the exact disposable company folder and dedicated test Hermes profile to run the first live native `/learn` pilot.
3. **Gate Inspection Automation:** Developing preflight validation scripts to detect native Hermes gate fail-open scenarios prior to dispatching agent turns.
4. **Founder Review UI:** Designing a unified review card surface displaying sources, missing gaps, staged native skill diffs, and held-out test evaluation results.