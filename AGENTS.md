# Factor

This repo is the framework. A company does not live here.

- `SOUL.md`, `config.yaml`, and `skills/` install as a Hermes profile: `hermes profile install <this-dir> --name factor --alias`
- `company/` is the blank glove. `scripts/new-company.sh <slug> <dest>` copies it.
- `connectors/` documents optional MCP servers, skills, and plugins. None are enabled by the profile.
- The older `snow-gloves-os` repo is a separate tree. This project does not import it.

After install, set the company path:

```bash
hermes -p factor config set skills.config.factor.company_root /absolute/path/to/company
```

Then point this profile at a Claude model, and a second profile at Codex. `docs/seats.md`.
