# Plan

Files: scripts/onboard.py, apps/mac/, specs/006-debug-rollback/spec.md.

Failure path: Rollback with no snapshot stops and says so. A bad apply leaves the previous owner page readable. The failed harvest sits beside the restored snapshot.

Implement only the tasks in tasks.md. Do not widen the spec in the same change.
