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
