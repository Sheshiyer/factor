# Tasks

Spec: 006-debug-rollback.

- F-45. A debug flag writes io/debug.log with the intent id and the check result.
- F-46. The log redacts anything that looks like a key or a token.
- F-47. A snapshot command copies raw, instinct.md, and profile-soul.md to rollback/last-good.
- F-48. Apply updates the snapshot only after the company check passes.
- F-49. A rollback command restores that snapshot and leaves the failed harvest beside it.
- F-50. Rollback refuses to run if no snapshot exists, and says so.
- F-51. The app has a Rollback item that calls that command.
- F-52. A broken apply leaves the previous wiki pages readable.
- F-53. Document the debug flag and rollback in this spec only.
- F-54. A test applies a bad harvest, rolls back, and finds the previous owner page.
- F-55. README stays the product story. Setup and debug stay below Begin and in the specs.
