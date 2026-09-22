# Connectors

`enabled.yaml` starts empty. The company works with no third-party tools.

When the founder turns one on, add an entry:

```yaml
connectors:
  - id: composio
    kind: mcp
    risk: low
    approval: no
    notes: "Reads only. Name the tools in the Hermes MCP allowlist."
```

`approval: yes` is required for money, people, legal, public sends, and paid calls, whatever `risk` says.

Turn tools on from the framework repo. Skills, plugins, and other capabilities are separate screens. The chosen cards are copied into this company's `skills/` folder.

```bash
scripts/onboard.py --company /absolute/path/to/this/company
```

An agent can do the same without a terminal picker:

```bash
scripts/onboard.py --text --category skills
scripts/onboard.py --company /absolute/path/to/this/company --enable openspec
```

How each id attaches: the framework file `connectors/catalog.md`. Composio is `connectors/composio.example.yaml` and is not part of that catalog.
