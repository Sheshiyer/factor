# Factor tasks

Eighty tasks. Grouped by release, wave, and swarm.

Owner for every task is the founder. Hours are 4 unless the id is a door or a first room template, which are 8: R2-W2-M-01, R2-W3-R-01, R3-W1-C-01, R3-W2-N-01.

Proof for a task is the validation line. A wave is done when each of its tasks has that proof.

## R1 Wave 1, product swarm

### R1-W1-P-01 State the three memory budgets in SOUL.md
- Area: product. Depends on: none.
- Deliverable: SOUL.md names one screen, 80 lines, and one page.
- Acceptance: A reader can point at the three budgets.
- Validation: Read SOUL.md.

### R1-W1-P-02 State the same budgets on the product README
- Area: product. Depends on: R1-W1-P-01.
- Deliverable: The README section on how a job enters matches the budgets.
- Acceptance: The README uses those sizes and adds no extra layer.
- Validation: Read README.md.

### R1-W1-P-03 Keep the harvest as an interview before the file
- Area: product. Depends on: none.
- Deliverable: Both harvest prompts ask one question at a time, then write factor-harvest.md.
- Acceptance: The prompts forbid guessing a style from adjectives.
- Validation: Read both harvest prompts.

### R1-W1-P-04 Name factor-harvest.md as the only handoff
- Area: product. Depends on: R1-W1-P-03.
- Deliverable: The Begin section says the project returns one file.
- Acceptance: No second handoff format is documented.
- Validation: Read README.md.

### R1-W1-P-05 List job inputs as room, sentence, and pages
- Area: data. Depends on: R1-W1-P-04.
- Deliverable: io/in.md contains those three fields.
- Acceptance: Apply writes io/in.md with the room list.
- Validation: The harvest unittest.

### R1-W1-P-06 List job outputs as draft, pages, amounts, and confidence
- Area: data. Depends on: R1-W1-P-05.
- Deliverable: io/out.md requires a page for every number.
- Acceptance: The file states a number with no page fails.
- Validation: Read io/out.md from a test company.

### R1-W1-P-07 Keep the room order in desks/README.md
- Area: product. Depends on: none.
- Deliverable: Content or numbers first. Partners and money last.
- Acceptance: The six room names match the README table.
- Validation: Compare the two lists.

### R1-W1-P-08 Tell the founder where to paste the profile soul
- Area: product. Depends on: R1-W1-P-01.
- Deliverable: The company SOUL.md points at profile-soul.md.
- Acceptance: The paste target is the Hermes profile.
- Validation: Read the generated SOUL.md.

## R1 Wave 1, data swarm

### R1-W1-D-01 Fail the check when the profile soul exceeds 80 lines
- Area: qa. Depends on: R1-W1-P-08.
- Deliverable: check_company.py reports an oversized profile soul.
- Acceptance: A fixture over 80 lines fails. A short fixture passes.
- Validation: unittest.

### R1-W1-D-02 Fail the check when instinct exceeds one screen
- Area: qa. Depends on: R1-W1-P-01.
- Deliverable: check_company.py reports an oversized instinct.md.
- Acceptance: A 50-line instinct fails. A short one passes.
- Validation: unittest.

### R1-W1-D-03 Resolve each index wikilink to a file
- Area: data. Depends on: R1-W1-P-05.
- Deliverable: Every wikilink in wiki/index.md has a matching markdown file.
- Acceptance: A missing target is reported.
- Validation: unittest.

### R1-W1-D-04 Keep the corrections table header stable
- Area: data. Depends on: none.
- Deliverable: wiki/corrections.md has Original, Rewrite, and Reason.
- Acceptance: Re-apply does not wipe existing rows.
- Validation: unittest.

### R1-W1-D-05 Copy the harvest into raw unchanged
- Area: data. Depends on: none.
- Deliverable: raw/harvest.md matches the input file bytes.
- Acceptance: A changed byte fails the test.
- Validation: unittest.

### R1-W1-D-06 Re-apply keeps projects and appends the log
- Area: data. Depends on: R1-W1-D-05.
- Deliverable: A hand-written project file survives a second apply.
- Acceptance: wiki/log.md gains one line and does not duplicate it.
- Validation: unittest.

## R1 Wave 2, Jev swarm

### R1-W2-J-01 Restrict the room question to named rooms
- Area: backend. Depends on: R1-W1-P-07.
- Deliverable: jev-gate lists only the six rooms plus the harvest desk.
- Acceptance: The skill contains that closed list.
- Validation: Read skills/jev-gate/SKILL.md.

### R1-W2-J-02 Restrict the page question to index lines
- Area: backend. Depends on: R1-W1-D-03.
- Deliverable: Page options come from wiki/index.md.
- Acceptance: The skill forbids inventing a page.
- Validation: Read the skill.

### R1-W2-J-03 Write 0.5 and 0.85 as the only thresholds
- Area: backend. Depends on: none.
- Deliverable: The skill and io/out.md use the same two numbers.
- Acceptance: A test reads both files and compares them.
- Validation: unittest.

### R1-W2-J-04 Stop when the TypeSafe skill is absent
- Area: backend. Depends on: none.
- Deliverable: The skill prints the npx install command and stops.
- Acceptance: It does not tell Claude to imitate Jev.
- Validation: Read the skill.

### R1-W2-J-05 Keep or drop tool lines without summarizing
- Area: backend. Depends on: none.
- Deliverable: Compaction keeps original text.
- Acceptance: A summary is named only as the thing to avoid.
- Validation: Read the skill.

### R1-W2-J-06 Forbid Jev from prices and claims
- Area: backend. Depends on: R1-W2-J-04.
- Deliverable: The Never section covers prices and claims.
- Acceptance: An example shows a rejected price question.
- Validation: Read the skill.

### R1-W2-J-07 Define the log line as pass, fail, or could not tell
- Area: backend. Depends on: none.
- Deliverable: evals/checks.md and the skill share that trio.
- Acceptance: No fourth status is named.
- Validation: Read both files.

### R1-W2-J-08 Keep writing on Claude and Codex
- Area: product. Depends on: R1-W2-J-06.
- Deliverable: The README says Jev picks and scores.
- Acceptance: The product page does not call Jev the writer.
- Validation: Read README.md.

## R1 Wave 2, QA swarm

### R1-W2-Q-01 Assert apply writes io and evals
- Area: qa. Depends on: R1-W1-P-06.
- Deliverable: The harvest test checks io/in.md, io/out.md, and evals/checks.md.
- Acceptance: unittest covers those paths.
- Validation: python3 -m unittest.

### R1-W2-Q-02 Fail an unsourced dollar amount
- Area: qa. Depends on: R1-W2-Q-01.
- Deliverable: A draft containing $99 fails when the offer has no $99.
- Acceptance: The message names the amount and the file.
- Validation: unittest.

### R1-W2-Q-03 Pass an amount that exists on a source page
- Area: qa. Depends on: R1-W2-Q-02.
- Deliverable: A draft that repeats a price from context/offer.md passes the money check.
- Acceptance: The money check is silent for that amount.
- Validation: unittest.

### R1-W2-Q-04 Report FILL used as a fact in a draft
- Area: qa. Depends on: none.
- Deliverable: A draft that states a FILL line as true is reported.
- Acceptance: The check names the draft.
- Validation: unittest.

### R1-W2-Q-05 Keep refusing shelf connectors
- Area: qa. Depends on: none.
- Deliverable: Enabling goose still exits non-zero.
- Acceptance: The existing test stays green.
- Validation: unittest.

### R1-W2-Q-06 Keep the non-interactive onboard path
- Area: qa. Depends on: none.
- Deliverable: A pipe with no flags exits 0 and prints the steps.
- Acceptance: The existing test stays green.
- Validation: unittest.

## R1 Wave 3, CI swarm

### R1-W3-C-01 Add a GitHub Action that runs unittest
- Area: infra. Depends on: R1-W2-Q-01.
- Deliverable: .github/workflows/test.yml runs python3 -m unittest discover tests.
- Acceptance: A push to main runs the workflow.
- Validation: gh run list.

### R1-W3-C-02 Fail the Action when the money check fails
- Area: infra. Depends on: R1-W3-C-01, R1-W2-Q-02.
- Deliverable: The workflow includes the unsourced-amount test.
- Acceptance: A broken fixture fails the Action.
- Validation: Workflow log.

### R1-W3-C-03 Confirm the three README images are in assets
- Area: product. Depends on: none.
- Deliverable: The morning, doors, and instinct images exist.
- Acceptance: The README links resolve.
- Validation: ls assets.

### R1-W3-C-04 Keep the MIT license file
- Area: infra. Depends on: none.
- Deliverable: LICENSE is MIT and the badge points at it.
- Acceptance: The GitHub license API returns MIT.
- Validation: gh api.

### R1-W3-C-05 Keep catalog cards out of the profile skill path
- Area: infra. Depends on: none.
- Deliverable: distribution.yaml owns skills and not catalog.
- Acceptance: skills/catalog does not exist.
- Validation: test -e.

### R1-W3-C-06 Point temperance-next-wave at Release 1 wave 1
- Area: infra. Depends on: R1-W1-P-01.
- Deliverable: STATE.md focus lists R1-W1-P-01 through R1-W1-D-06.
- Acceptance: temperance-next-wave --cwd . prints that focus.
- Validation: CLI.

## R1 Wave 3, copy swarm

### R1-W3-K-01 Match the README inception section to io/in.md
- Area: product. Depends on: R1-W1-P-05.
- Deliverable: Room, sentence, and pages appear in both.
- Acceptance: The words match.
- Validation: Side-by-side read.

### R1-W3-K-02 Keep setup commands below the product story
- Area: product. Depends on: none.
- Deliverable: Begin is the first command block.
- Acceptance: No install guide sits above the rooms.
- Validation: Read README.md.

### R1-W3-K-03 Say approval before the setup commands
- Area: product. Depends on: none.
- Deliverable: Sending, spending, and publishing wait is above Begin.
- Acceptance: The sentence is present.
- Validation: Read README.md.

### R1-W3-K-04 Match the room table to desks/README.md
- Area: product. Depends on: R1-W1-P-07.
- Deliverable: The six names and the start order agree.
- Acceptance: The names are the same list.
- Validation: Compare the names.

## R2 Wave 1, intent swarm

### R2-W1-I-01 Define the intent fields
- Area: data. Depends on: R1-W3-K-01.
- Deliverable: Sentence, room, and source door are the required fields.
- Acceptance: A sample file validates.
- Validation: unittest.

### R2-W1-I-02 Reject an unknown room
- Area: data. Depends on: R2-W1-I-01.
- Deliverable: A room outside the list fails the check.
- Acceptance: The error names the room.
- Validation: unittest.

### R2-W1-I-03 Add one sample intent per door
- Area: product. Depends on: R2-W1-I-01.
- Deliverable: io/examples holds mac, raycast, and hermes samples.
- Acceptance: The three files share the same sentence.
- Validation: Read the files.

### R2-W1-I-04 Keep the wiki out of the intent
- Area: data. Depends on: R2-W1-I-01.
- Deliverable: The schema has page names, not page bodies.
- Acceptance: A body field is rejected.
- Validation: unittest.

### R2-W1-I-05 Define the response fields
- Area: data. Depends on: R1-W1-P-06.
- Deliverable: Draft path, pages, amounts, and confidence.
- Acceptance: A sample response validates.
- Validation: unittest.

### R2-W1-I-06 Fail a response whose amount has no page
- Area: qa. Depends on: R2-W1-I-05.
- Deliverable: The checker names the amount.
- Acceptance: The response does not ship.
- Validation: unittest.

### R2-W1-I-07 Keep the schema in io/
- Area: product. Depends on: R2-W1-I-01.
- Deliverable: No new protocol document is added.
- Acceptance: io/in.md and io/out.md are the contract.
- Validation: ls.

### R2-W1-I-08 Round-trip one intent into one response shape
- Area: qa. Depends on: R2-W1-I-03, R2-W1-I-05.
- Deliverable: A fixture intent produces the response keys.
- Acceptance: The keys match io/out.md.
- Validation: unittest.

## R2 Wave 2, Mac swarm

### R2-W2-M-01 Add a menu-bar applet with one text field
- Area: frontend. Depends on: R2-W1-I-01. Hours: 8.
- Deliverable: The applet shows a field and a submit control.
- Acceptance: A local build launches.
- Validation: Launch log.

### R2-W2-M-02 Write an intent file on submit
- Area: frontend. Depends on: R2-W2-M-01.
- Deliverable: Submit writes the shared intent JSON into the company io folder.
- Acceptance: The file matches the schema.
- Validation: Fixture compare.

### R2-W2-M-03 Do not call a model from the applet
- Area: frontend. Depends on: R2-W2-M-02.
- Deliverable: The applet source has no model client.
- Acceptance: Search finds no provider URL.
- Validation: rg.

### R2-W2-M-04 Show waiting, ready, or needs you
- Area: frontend. Depends on: R2-W2-M-02.
- Deliverable: The menu subtitle is one of those three states.
- Acceptance: A fixture status file changes the subtitle.
- Validation: Manual check.

### R2-W2-M-05 Document local-only signing for the first build
- Area: infra. Depends on: R2-W2-M-01.
- Deliverable: A short note says the first build is unsigned and local.
- Acceptance: The note sits next to the applet, not on the product page.
- Validation: Read the note.

### R2-W2-M-06 Read the instinct first line for the subtitle
- Area: frontend. Depends on: R2-W2-M-04.
- Deliverable: The menu can show the instinct Who line.
- Acceptance: A changed instinct line changes the subtitle.
- Validation: Fixture.

### R2-W2-M-07 Test the intent file the applet writes
- Area: qa. Depends on: R2-W2-M-02.
- Deliverable: A golden file matches the writer.
- Acceptance: The test fails if the door field changes.
- Validation: unittest.

## R2 Wave 3, Raycast swarm

### R2-W3-R-01 Add a Raycast script command for one sentence
- Area: frontend. Depends on: R2-W1-I-01. Hours: 8.
- Deliverable: The command accepts the job as text.
- Acceptance: Running it writes an intent.
- Validation: Command log.

### R2-W3-R-02 Write the same intent JSON as the applet
- Area: frontend. Depends on: R2-W3-R-01, R2-W2-M-02.
- Deliverable: Both writers share one schema.
- Acceptance: A diff of the two outputs shows only the source door.
- Validation: unittest.

### R2-W3-R-03 Offer the six rooms as the command argument
- Area: frontend. Depends on: R2-W3-R-01.
- Deliverable: The argument list is the room names.
- Acceptance: An unknown room is refused.
- Validation: Command help.

### R2-W3-R-04 Keep secrets out of the Raycast folder
- Area: infra. Depends on: R2-W3-R-01.
- Deliverable: No key, token, or env file is in the folder.
- Acceptance: Search is empty.
- Validation: rg.

### R2-W3-R-05 Name Raycast on the product page without a setup guide
- Area: product. Depends on: R2-W3-R-01.
- Deliverable: The doors table has one row for Raycast.
- Acceptance: Begin does not grow a Raycast tutorial.
- Validation: Read README.md.

### R2-W3-R-06 Map Raycast arguments onto io/in.md
- Area: qa. Depends on: R2-W3-R-02.
- Deliverable: A fixture argv becomes room, sentence, and source door.
- Acceptance: The fields match io/in.md.
- Validation: unittest.

## R2 Wave 4, Hermes swarm

### R2-W4-H-01 Add a Hermes skill that reads an intent file
- Area: backend. Depends on: R2-W1-I-01.
- Deliverable: The skill loads the intent JSON.
- Acceptance: A missing file stops with the path.
- Validation: Read the skill.

### R2-W4-H-02 Load instinct, then the index, then one page
- Area: backend. Depends on: R2-W4-H-01.
- Deliverable: The skill procedure is those three reads.
- Acceptance: It forbids loading the whole wiki.
- Validation: Read the skill.

### R2-W4-H-03 Open a card with the five fields already used
- Area: backend. Depends on: R2-W4-H-02.
- Deliverable: Desk, seat, done, read, and write are on the card.
- Acceptance: A fixture body lists them.
- Validation: Read the skill and the fixture.

### R2-W4-H-04 Request review before the card can complete
- Area: backend. Depends on: R2-W4-H-03.
- Deliverable: The skill cites the open-card review rule.
- Acceptance: Both skills agree.
- Validation: Read both skills.

### R2-W4-H-05 Stay quiet when the numbers room has nothing to report
- Area: product. Depends on: R2-W4-H-02.
- Deliverable: The skill says a healthy room sends nothing.
- Acceptance: The sentence is present.
- Validation: Read the skill.

### R2-W4-H-06 Prove applet and Hermes intents share card fields
- Area: qa. Depends on: R2-W2-M-07, R2-W4-H-03.
- Deliverable: Two fixtures differ only by source door.
- Acceptance: The card bodies match on desk, done, read, and write.
- Validation: unittest.

## R3 Wave 1, content swarm

### R3-W1-C-01 Add a weekday content brief template
- Area: product. Depends on: R2-W4-H-03. Hours: 8.
- Deliverable: The template is a short list, not fifty ideas.
- Acceptance: It has a place for keep, drop, or develop.
- Validation: Read the template.

### R3-W1-C-02 Require the brief to cite pages
- Area: data. Depends on: R3-W1-C-01.
- Deliverable: Each item names a wiki or context page.
- Acceptance: An item without a page fails the check.
- Validation: unittest.

### R3-W1-C-03 Record keep, drop, or develop as a card comment
- Area: product. Depends on: R3-W1-C-01.
- Deliverable: The founder's choice is a comment.
- Acceptance: The brief itself does not publish.
- Validation: Read the template.

### R3-W1-C-04 Block publish from the content room
- Area: backend. Depends on: R3-W1-C-03.
- Deliverable: The room playbook says drafts wait.
- Acceptance: No send step is in the template.
- Validation: Read the playbook.

### R3-W1-C-05 Fail a content brief that cites no page for a stat
- Area: qa. Depends on: R3-W1-C-02, R1-W2-Q-02.
- Deliverable: An unsourced figure fails the fact check.
- Acceptance: The message names the figure.
- Validation: unittest.

## R3 Wave 2, numbers swarm

### R3-W2-N-01 Define the numbers output as figures plus pages
- Area: data. Depends on: R2-W1-I-05. Hours: 8.
- Deliverable: Each figure has a page field.
- Acceptance: A figure without a page fails.
- Validation: unittest.

### R3-W2-N-02 Separate a suggestion from the figure
- Area: product. Depends on: R3-W2-N-01.
- Deliverable: The suggestion is a second block.
- Acceptance: The figure block has no advice mixed in.
- Validation: Read the template.

### R3-W2-N-03 Stop the room when a source page is missing
- Area: backend. Depends on: R3-W2-N-01.
- Deliverable: The playbook says stop and name the page.
- Acceptance: A fixture missing a page fails.
- Validation: unittest.

### R3-W2-N-04 Stay quiet when no line was crossed
- Area: product. Depends on: R2-W4-H-05.
- Deliverable: The numbers playbook repeats the quiet rule.
- Acceptance: The sentence is present.
- Validation: Read the playbook.

### R3-W2-N-05 Write an eval row for a numbers run
- Area: qa. Depends on: R1-W2-J-07.
- Deliverable: wiki/log.md receives pass, fail, or could not tell.
- Acceptance: A fixture appends one line.
- Validation: unittest.

## R3 Wave 3, approval swarm

### R3-W3-A-01 Add send, spend, and publish to the card checklist
- Area: product. Depends on: R2-W4-H-04.
- Deliverable: The card body has those three gates.
- Acceptance: Each gate is wait or approved.
- Validation: Read the template.

### R3-W3-A-02 Block completion under 0.85 without a yes
- Area: backend. Depends on: R3-W3-A-01, R1-W2-J-03.
- Deliverable: The jev-gate and the card use 0.85.
- Acceptance: A lower confidence cannot complete.
- Validation: Read the skill and the fixture.

### R3-W3-A-03 Let an approval comment unblock the card
- Area: backend. Depends on: R3-W3-A-02.
- Deliverable: A founder comment is enough.
- Acceptance: The worker still cannot complete alone.
- Validation: Read open-card and jev-gate.

### R3-W3-A-04 Keep the partners room from sending the brief
- Area: product. Depends on: R3-W1-C-04.
- Deliverable: The partners playbook drafts and waits.
- Acceptance: No send step.
- Validation: Read the playbook.

### R3-W3-A-05 Draft the money follow-up and wait
- Area: product. Depends on: R3-W3-A-04.
- Deliverable: The money playbook drafts the chase and waits for one yes.
- Acceptance: No send step.
- Validation: Read the playbook.
