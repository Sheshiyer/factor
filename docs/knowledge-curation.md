# Local knowledge curation and content review

Factor stores a company's sources, claims and corrections inside that company's root. The following commands use Python's standard library. They make local files only: no Hermes/provider invocation, scheduler, send, spend or publication is implemented.

Run from the Factor checkout. Use an existing company root or create a disposable company for the walkthrough:

```sh
COMPANY_TRIAL=$(mktemp -d)/example
scripts/new-company.sh example "$COMPANY_TRIAL"
mkdir -p "$COMPANY_TRIAL/wiki"
printf '\n[Trial voice](trial-voice.md)\n' >> "$COMPANY_TRIAL/wiki/index.md"
printf '# Trial voice\nUse concrete language.\n' > "$COMPANY_TRIAL/wiki/trial-voice.md"
```

## Intake, exact revisions and human review

The source body is data. It cannot install a skill or change policy. Unknown publication and effective dates remain unknown. Omit `--body` for missing source text; retrieval exposes the resulting gap. Importing unchanged source bytes is idempotent; a changed body creates an immutable revision, and claims tied to older versions need fresh review.

```sh
SOURCE_REVISION=$(python3 scripts/knowledge.py --root "$COMPANY_TRIAL" import-source \
  --id trial-source --url https://example.test/report --author Founder \
  --body 'The product has three rooms.' --completeness complete \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["revision"])')

python3 scripts/knowledge.py --root "$COMPANY_TRIAL" add-claim \
  --id room-count --subject product --predicate room-count \
  --statement 'The product has three rooms.' --source-id trial-source \
  --source-revision "$SOURCE_REVISION" --locator 'paragraph 1' --page trial-voice.md

python3 scripts/knowledge.py --root "$COMPANY_TRIAL" review \
  --claim-id room-count --status accepted
python3 scripts/knowledge.py --root "$COMPANY_TRIAL" retrieve --page trial-voice.md
```

Only mark a claim accepted after human review. Newly captured, disputed and rejected claims are ineligible. Retrieval requires an indexed wiki page and exposes conflicting accepted statements sharing a subject/predicate. Source IDs, revision digests and locators are attribution evidence; they do not prove semantic truth or automatically validate every number in prose.

## Assemble the supplied draft

The founder supplies the text and card identity. The CLI does not pretend to have generated an LLM draft or create an approval from the card name.

```sh
python3 scripts/content_trial.py --root "$COMPANY_TRIAL" --page trial-voice.md \
  --card-id content-trial-1 \
  --text 'Amazing product. It has three rooms. [Report](https://example.test/report)'
```

Alternatively, save the text beneath the company root and use `--draft-file input/draft.md`. Paths are company-relative; traversal and symbolic links in the consumed wiki tree or output path are rejected. `--output-dir` may select another directory beneath `output/`.

The returned path points to a JSON review packet under `output/content-trials/`. It contains the supplied prose after accepted corrections, accepted claims, source revision evidence, gaps, conflicts, and explicit `local_only`, `published: false` and empty `external_actions` fields. Gaps, conflicts or absence of accepted claims produce a blocked packet with no draft and exit code 1. Invalid input/path failures exit 2.

Each filename contains the SHA-256 of the canonical input and the SHA-256 of the actual packet. Repeating unchanged input and output reuses the same file without rewriting it; a changed corrected draft produces another packet. Existing content-addressed files with altered bytes are rejected. Run receipts expose `deduplicated` and both digests. No approval is copied forward to a changed packet.

## Record, propose, accept and replay corrections

A correction records the original, rewrite, reason, page scope and a regression example. Repeated evidence proposes a rule; proposal alone cannot change the next draft. The examples below represent two separately reviewed examples:

```sh
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

The next packet says “Useful product.” Accepted rules are page-scoped and guarded by the exact reviewed page digest. Contradictory rewrites require review. The trial protects Markdown links, wiki links, reference citations, URLs and code spans from prose corrections; its conservative markup handling is not a full Markdown renderer. The lower-level `apply-corrections` CLI performs text replacement, so use the trial for citation-bearing content:

```sh
python3 scripts/corrections.py "$COMPANY_TRIAL" apply-corrections \
  --page trial-voice.md --text 'Amazing product.'
```

## Local approval validation

Send, spend and publish always require human approval. These primitives bind a root identity, card, action, target, canonical payload digest, approver and expiry. The local store is a trusted-caller boundary; it does not authenticate the named approver or supply an external executor, signature, one-time consumption or transport. Do not treat a synthetic/local fixture as permission to act.

After an actual human approval, create a record using the exact approved payload and expiry (the example creates only a disposable local record):

```sh
APPROVAL_EXPIRY=$(python3 -c 'from datetime import datetime,timedelta,timezone; print((datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat())')
python3 scripts/approvals.py make "$COMPANY_TRIAL" content-trial-1 publish local-review Founder \
  "$APPROVAL_EXPIRY" --payload-json '{"text":"Useful product."}'
python3 scripts/approvals.py list "$COMPANY_TRIAL"
```

Copy the returned approval ID for validation:

```sh
python3 scripts/approvals.py validate "$COMPANY_TRIAL" content-trial-1 publish local-review \
  "$APPROVAL_ID" --payload-json '{"text":"Useful product."}'
```

A changed root, card, action, target, payload or expired record invalidates approval. Confidence cannot bypass it. The content trial itself has no publish operation.

## Jev shadow fixtures and context preservation

The CLI validates supplied results only; it makes no provider calls. Synthetic fixtures stay explicitly synthetic and shadow-only. Non-synthetic receipts require provider/model attribution, which is caller-supplied evidence rather than independent proof of a network call.

```sh
python3 scripts/jev_decisions.py validate-decision \
  '{"outcome":"candidate-a","confidence":0.8,"synthetic":true}' candidate-a,candidate-b
python3 scripts/jev_decisions.py validate-decision '{"outcome":"timeout"}' candidate-a,candidate-b
python3 scripts/jev_decisions.py compact-context \
  '[{"id":"one","content":"Do not publish."},{"id":"two","content":"Draft discussion"}]' \
  one ranking_fail
```

Disabled, unavailable, timeout, abstention, invalid candidates, invalid confidence and low confidence are explicit outcomes. Failed ranking retains all messages; successful selection preserves original kept message values and protected constraints. JSON CLI serialization may change whitespace around the envelope; it does not rewrite message content.

## Verification and limits

```sh
python3 -m unittest discover -s tests -p 'test_content_trial.py' -v
python3 -m unittest discover -s tests -v
```

The integration tests exercise intake → review → draft → accepted correction → next draft, stale/missing/conflicting evidence, citations, output deduplication, packet tampering and path containment. Storage assumes one writer at a time and a privileged, trusted local caller. Filesystem operations assume no concurrent attacker swapping directories between checks; this is not a multi-user filesystem sandbox. Existing prose citations and factual entailment still need human review. No live Hermes, Jev, connector, browser, publishing or scheduling acceptance is implied. Cached research and missing article bodies remain incomplete until separately refreshed.
