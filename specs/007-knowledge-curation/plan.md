# Implementation plan

Inputs: docs/research/2026-09-27-agent-knowledge/, .planning/GITHUB-RECONCILIATION.md, specs/002-memory, specs/003-jev, specs/004-evals, specs/006-rooms, tasks/lessons.md. Current baseline: 30 unit tests pass.

## Parallel wave: isolated noesis-execute worktrees

A owns scripts/knowledge.py and tests/test_knowledge.py only. Expose import_source(root, record), add_claim(root, claim), review_claim(root, claim_id, status), retrieve(root, page). Store root/wiki/knowledge.json atomically with source revisions, claims, review status. Source input fields: id,url,author,published_at,body,completeness; body may be null with explicit missing status. Return source revision digest. Claim fields: id,subject,predicate,statement,source_id,source_revision,locator,effective_at,page. Use safe rooted file operations. retrieve returns dict with page,text,claims,gaps,conflicts, source revision evidence; only accepted claims eligible; conflicts not suppressed. API accepts Path root. CLI subcommands import-source/add-claim/review/retrieve.

B owns scripts/approvals.py, tests/test_approvals.py, scripts/onboard.py, scripts/rooms.py, tests/test_rooms.py, docs/rooms.md, company/desks/gates.md, skills/jev-gate/SKILL.md, specs/003-jev/spec.md only. Expose payload_digest(payload), make_approval(root,card_id,action,target,payload,approver,expires_at), validate_approval(root,card_id,action,target,payload,approval,now=None) -> bool. A confidence argument cannot authorize. Reject malformed/expired/mismatched approvals and non-finite payloads. Document trusted caller boundary. Reconcile confidence-or-approval language and legacy tests without weakening founder authority. No actual external adapter.

C owns scripts/corrections.py, scripts/jev_decisions.py, tests/test_corrections.py, tests/test_jev_decisions.py only. Corrections: record_correction(root,record), propose_rule(root,scope,reason), accept_rule(root,proposal_id,approver,expected_sha256), apply_corrections(root,page,text). Records original,rewrite,reason,scope relative wiki page. Store proposals under wiki, expected digest guard preserves source; accepted rule should affect apply_corrections and append reviewed rule to page, preserving unrelated bytes. Conflicting rewrite for same original must not auto-promote. Jev: validate_decision(candidates,result,min_confidence=0.5) -> explicit status dict, shadow_only; require finite [0,1] confidence, matching candidate, proper provider/model receipt for real results, synthetic label for local fixtures. compact_context(messages,keep_ids,ranking_ok) -> original messages with protected entries and full fallback.

Every worker is not alone in the codebase, must preserve others' edits, and must read this spec. No worker changes planning/ISA or other assigned files. No new dependencies. Tests must cover behavior and failure boundaries, not only string presence.

## Integration wave

Review gateway attribution and diffs before accepting output. Integrate independently. Add scripts/content_trial.py, tests/test_content_trial.py and docs/knowledge-curation.md around the actual APIs. Run temp-company source -> claim -> review -> draft -> correction -> next draft; prove cited source versions and unchanged-run dedup. Review malicious paths, invalid provenance, conflicts, approval digest changes and failed ranker preservation. Run complete unittest suite once integrated. Record local evidence; no claim of live Hermes/Jev/connector acceptance.

## Deferred research

Source refresh authentication, missing article bodies, authenticated approval transport/one-time consumption at an eventual executor, provider calibration, semantic number entailment beyond explicit claim attribution, proven routine scheduling and Grok bridge remain separate milestones. Never promote source-exact attribution as automatic truth verification.
