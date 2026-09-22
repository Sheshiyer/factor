# What you can add

The profile ships the operator skills and `catalog-onboard`. Offered cards live in `catalog/cards/` and are copied into a company only when onboarding selects them. Composio is a separate example in `composio.example.yaml` and is not in this catalog.

The catalog is the Field Theory bookmark cache, grouped for onboarding:

| Category | What it is |
|---|---|
| Skills | A `SKILL.md` the agent can load. The card points at the upstream pack. |
| Plugins | A plugin named in the cache. |
| Other capabilities | An MCP server, a CLI, or a directory of servers. |

`connectors/registry.yaml` is the full list, including rows already covered by Hermes and rows that are not offered. Onboarding:

```bash
scripts/onboard.py                         # picker in a terminal
scripts/onboard.py --text                  # agent-readable list
scripts/onboard.py --json --category skills
scripts/onboard.py --company ~/companies/acme --enable openspec,ffmpeg-skill
scripts/onboard.py --company ~/companies/acme --enable-category plugins
```

A pipe never waits for a keypress. Shelf ids and unknown ids are refused.

Add a capability in the thinnest form that works, on the company that needs it.

| Need | Add this | Leave it off when |
|---|---|---|
| Instructions for a repeated job | A `SKILL.md` on the profile, or under the company's `skills/` | The job happens once |
| A SaaS product, many of them through one login | Composio, as an MCP server. `connectors/composio.example.yaml` | The company has not named the tools |
| One remote or local tool server | `hermes mcp add` | A skill plus a CLI already does it |
| A reviewed server from Nous | `hermes mcp catalog`, then `hermes mcp install <name>` | You have not read its tool list |
| Code that must run the same way every time | A Hermes plugin (`plugin.yaml` plus `register`) | A skill can say the steps |
| Claude Code or Codex as a worker | The bundled `claude-code` and `codex` skills, already installable on a profile | You would be adding a third agent runtime |
| Mail, calendar, drive | The bundled Google Workspace skill, or Composio, after `enabled.yaml` says so | The company does not use that account |
| A standing Monday review | Accept the `weekly-review` blueprint with `/suggestions` | You want silence until you ask |
| Another memory backend | A Hermes memory provider | The company repo and `MEMORY.md` are enough |

Secrets go in `~/.hermes/profiles/factor/.env`. The company repo stores the connector id, the risk, and whether approval is required.

After adding an MCP server, limit the tools:

```bash
hermes -p factor mcp configure <name>
```

An allowlist that is empty of intention is how a connector grows past the company. Name the tools in `tools.include`.

Cron from a blueprint is a suggestion until you accept it. Installing this profile does not start a schedule.
