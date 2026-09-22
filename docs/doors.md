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
