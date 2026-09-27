# Install or upgrade Factor with your coding assistant

Open a terminal-capable coding session in the Factor checkout and paste the prompt below. It works with Codex, Claude Code, or another coding assistant that can inspect files and run commands. This is an instruction prompt, not a shell script. The assistant runs the appropriate commands after inspecting your installation.

For a new checkout:

```sh
git clone https://github.com/Sheshiyer/factor.git
cd factor
```

Copy everything between **BEGIN PROMPT** and **END PROMPT**. You can also tell your assistant: **“Read `prompt-install.md` and carry out its install-or-upgrade prompt.”**

## BEGIN PROMPT

Install or upgrade Factor from this repository and verify the result. Work through the steps below; execute the applicable commands, resolve routine problems, and report actual results. Do not stop at giving me a plan. Ask only for missing choices you cannot discover, credentials I must enter myself, or a consequential change outside the scope I selected.

### My setup

Use these values when provided; otherwise discover existing values before asking. Replace placeholders before running any command. Keep shell variables in the same session or pass resolved absolute paths to each command.

- Mode: auto-detect fresh install versus upgrade.
- Factor repository: the current checkout, resolved to an absolute path.
- Target version/ref: preserve an explicitly requested ref; otherwise use the verified remote default branch for a normal upgrade. Do not switch an intentional development branch silently.
- Company folder: reuse the configured external company folder. Ask for a slug and destination only if there is no company yet.
- Factor profile: `factor`, unless the existing installation uses another name.
- Coding profile: `coder`, optional; preserve the existing choice.
- Listener: the Hermes messaging gateway, reusing the host's existing service when it already serves this profile.
- Mac menu bar: launch if I selected that door; otherwise keep it available as an optional step.
- Language: English by default. Reuse the company preference; offer French without translating existing facts or identifiers.

Use task-specific variables such as `FACTOR_REPO`, `FACTOR_COMPANY`, `FACTOR_PROFILE`, `FACTOR_CODER_PROFILE`, `FACTOR_TARGET_REF`, and `FACTOR_BACKUP_DIR`. Do not repurpose `HOME`, `PATH`, or the coding assistant's configuration variables. Quote paths, including paths with spaces.

### 1. Inspect before changing anything

Read `AGENTS.md`, `README.md`, `distribution.yaml`, `docs/seats.md`, `config.yaml`, the scripts you will execute, and relevant door documentation. Treat the checked-out files and installed CLI help as authoritative; version-dependent commands may differ.

Record the repository path, branch, commit, remote, dirty/untracked state, OS, available Python, and installed Hermes version. Verify the remote is the intended Factor repository. Do not reset, clean, stash, overwrite, or include unrelated work automatically.

```sh
git -C "$FACTOR_REPO" status --short
git -C "$FACTOR_REPO" branch --show-current
git -C "$FACTOR_REPO" rev-parse HEAD
git -C "$FACTOR_REPO" remote -v
python3 --version
hermes --version
hermes profile list
hermes profile install --help
hermes profile update --help
hermes doctor --help
hermes gateway --help
```

Only run Hermes commands after confirming the executable exists. If Hermes is missing or incompatible with `hermes_requires` in `distribution.yaml`, explain that prerequisite and use the current official NousResearch Hermes installation instructions after checking their source. Download and inspect any installer before executing it. Never substitute a similarly named package. An existing Hermes runtime upgrade is a separate choice from updating Factor; preserve its version unless required and authorized.

For an existing Factor profile, inspect its distribution metadata and profile directory:

```sh
hermes profile info "$FACTOR_PROFILE"
hermes profile show "$FACTOR_PROFILE"
hermes -p "$FACTOR_PROFILE" gateway status
hermes gateway list
```

Distinguish a missing profile from a command failure. Inspect only the specific config fields needed; do not dump `.env`, auth files, or tokens into the conversation. Record the company path, model/provider selection, coder profile, dispatcher setting, gateway service owner, and whether the service is already running. Profile `-p` flags must be explicit; do not change the sticky default with `profile use`.

### 2. Protect an existing setup and choose the source

Before upgrading, make a private, timestamped backup outside both the repository and company directory. Back up the existing company folder and the effective Hermes profile state, including configuration, identity, skills, memories and credentials. Use `umask 077`; inspect the installed backup command's help and verify the archive is readable and contains the expected paths without printing secret contents.

For example, after assigning a unique backup directory and confirming the installed flags:

```sh
umask 077
mkdir -p "$FACTOR_BACKUP_DIR"
hermes -p "$FACTOR_PROFILE" backup -o "$FACTOR_BACKUP_DIR/hermes-profile.zip" --keep 0
tar -czf "$FACTOR_BACKUP_DIR/company.tar.gz" \
  -C "$(dirname "$FACTOR_COMPANY")" "$(basename "$FACTOR_COMPANY")"
```

Record the old Factor commit and distribution source. Inspect backup exclusions and inventory symlinked or externally stored skills/memory; archive their resolved targets separately when needed, or explicitly report them outside recovery coverage. Back up all state that would be affected by a shared gateway change; the profile backup alone must not be described as a backup of every host profile. Coordinate a quiet backup window if relevant processes are writing. A redacted `profile export` is not a complete recovery backup. Factor's `scripts/snapshot.py` only saves instinct, profile soul, and raw harvest data; it does not back up the entire company or Hermes state. Do not use it as the upgrade backup.

Fetch the verified remote. Advance only a clean checkout whose intended branch/ref is known, using a fast-forward update. If dirty, detached, divergent, or on an intentional development branch, preserve it and explain the exact choice needed; a separate clean checkout at the requested ref is preferable to destructive repair. Record the resolved target commit before updating the profile.

```sh
git -C "$FACTOR_REPO" fetch origin
# Only after the checkout, branch and target have passed the checks above:
git -C "$FACTOR_REPO" merge --ff-only "$FACTOR_TARGET_REF"
```

Fresh installs from a deliberately selected checkout use that checkout as-is. Do not merge merely because this prompt mentions upgrades.

### 3. Install fresh, or update the existing distribution

**Fresh profile only:** inspect the manifest and install from the verified local checkout. Do not overwrite a profile with the same name.

```sh
hermes profile install "$FACTOR_REPO" --name "$FACTOR_PROFILE" --alias
```

For a genuinely new company, select a destination outside Factor and outside the Hermes profile. Require it not to exist, then run the existing shell scaffold:

```sh
sh "$FACTOR_REPO/scripts/new-company.sh" "$FACTOR_COMPANY_SLUG" "$FACTOR_COMPANY"
```

Ask for an existing `factor-harvest.md`, or help me produce one using `prompts/harvest-claude.md` or `prompts/harvest-codex.md`. Apply only a supplied, reviewed harvest to this new company:

```sh
python3 "$FACTOR_REPO/scripts/onboard.py" --company "$FACTOR_COMPANY" \
  --apply-harvest "$FACTOR_HARVEST"
```

A blank company may correctly fail validation. Report the missing facts and request them; never invent company context to make a check pass.

**Existing distribution profile:** compare `hermes profile info`'s recorded source with the intended source first. `profile update` reads that recorded source, not necessarily the checkout in this session. A local-directory source must point to the reviewed checkout; a Git URL source may fetch a moving default branch instead of a requested commit. If source or version cannot be matched, stop the profile mutation and explain the mismatch. Do not silently reinstall with `--force` or retarget distribution metadata.

```sh
hermes profile update "$FACTOR_PROFILE"
```

Use the normal update path without `--force-config`. It preserves `config.yaml`, but distribution-owned files such as `SOUL.md` and shipped skills can be replaced. Compare local edits to those files before updating and preserve/reconcile them explicitly. User skills, sessions, memory, credentials, and company data must remain intact. Do not recreate the company, reapply harvest, or copy the blank `company/` tree over an existing company during an upgrade.

Compare the preserved config with the new template. Apply only required, understood changes and preserve model/provider, company path, approvals, connectors, and user overrides. Report proposed changes that would enable new behavior.

### 4. Bind the company and seats

For a new profile, set its company path; for an upgrade, verify the existing value and change it only when the selected destination differs.

```sh
hermes -p "$FACTOR_PROFILE" config set skills.config.factor.company_root "$FACTOR_COMPANY"
hermes -p "$FACTOR_PROFILE" config set skills.config.factor.framework_root "$FACTOR_REPO"
```

On a fresh profile, use `hermes -p "$FACTOR_PROFILE" model` to choose the intended Claude provider/model. Preserve the existing model on upgrades. Let me complete interactive authentication privately; never request that I paste credentials into chat.

If I choose the coding seat, follow `docs/seats.md`. Create and configure it only when missing:

```sh
hermes profile create "$FACTOR_CODER_PROFILE" --no-skills \
  --description "Codex build seat. Takes Factor cards that say seat codex."
hermes -p "$FACTOR_CODER_PROFILE" model
```

For either a newly created or existing selected coding profile, verify its identity/model, preserve an existing provider selection, and verify or set the Factor binding:

```sh
hermes -p "$FACTOR_PROFILE" config set skills.config.factor.codex_profile "$FACTOR_CODER_PROFILE"
```

Run the create command only for a missing coding profile. Keep one Factor board dispatcher; do not start a second dispatcher on the coding seat. Optional connectors and catalog skills stay unselected until the company chooses them. Do not enable the whole catalog, schedules, background learning, messaging platforms, or new external actions as a side effect of setup.

### 5. Choose the language, offer learning resources, and run checks

Offer the framework and operator guides from `docs/learning.md` or `docs/learning.fr.md` before the first task. List resources with `python3 "$FACTOR_REPO/scripts/onboard.py" --company "$FACTOR_COMPANY" --resources`; open a selected resource only when requested using `--open-resource ID`. If I choose French, persist it with `python3 "$FACTOR_REPO/scripts/onboard.py" --company "$FACTOR_COMPANY" --set-language fr`; use `en` to switch back. Preserve an existing choice on upgrade. Mac, CLI and Hermes use `<company>/preferences.json`. The video/decks/infographics are currently French-only and must be labeled that way. The bundled files do not require NotebookLM access.

Run the following checks:

```sh
hermes -p "$FACTOR_PROFILE" doctor
python3 "$FACTOR_REPO/scripts/check_company.py" "$FACTOR_COMPANY"
python3 "$FACTOR_REPO/scripts/rooms.py" "$FACTOR_COMPANY"
python3 "$FACTOR_REPO/scripts/onboard.py" --text
```

Capture actual output and exit status. Classify missing optional credentials separately from blockers. Inspect each proposed repair before applying it; do not blanket-run `doctor --fix`, `--live`, or acknowledge advisories automatically. Report each failing check and its cause. The room checker only checks files that exist, so it cannot establish that every room is configured or running.

### 6. Bring up or refresh the Hermes listener

The listener is the **Hermes gateway**. There is no Factor-specific `listener` executable. Inspect current CLI help and `gateway list` before changing service state. Identify whether this profile is already served by a host multiplexer or owns a separate service. Reuse the existing topology; never create a second poller for the same bot credentials.

Starting a configured gateway may process messages and queued cron/kanban work. Inspect that scope first. Continue when my selected setup authorizes starting this profile and its configured work; ask before enabling new channels or restarting a shared host service that would interrupt unrelated profiles. Never use `gateway start --all`, `--force`, or a host-wide migration as a routine setup shortcut.

Run commands against the discovered **service-owning profile**, which may differ from the Factor profile. Assign `FACTOR_GATEWAY_PROFILE` accordingly. On a genuinely fresh host with no gateway owner, select the Factor profile as the owner unless the installed Hermes topology requires a host multiplexer; inspect that topology before installation.

If no messaging channel is configured, ask which platform I want to connect. Once selected, inspect `gateway setup --help` and run `hermes -p "$FACTOR_GATEWAY_PROFILE" gateway setup` interactively, letting me enter credentials privately. This platform choice authorizes configuring that channel only. If I defer it, report messaging as pending instead of claiming a working listener.

```sh
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway status
# Existing service, currently stopped, and its start is in scope:
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway start
# Existing running service, only if changes require reload and interruption is in scope:
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway restart
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway status
hermes -p "$FACTOR_PROFILE" status
```

Choose **start or restart when needed**, not both. A healthy unchanged listener needs neither. If no service exists and background operation was selected, inspect `gateway install --help`, install with explicit startup choices, then start it. On supported versions:

```sh
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway install --no-start-now --no-start-on-login
hermes -p "$FACTOR_GATEWAY_PROFILE" gateway start
```

Enable start-on-login only when selected. For a foreground/container setup, use `hermes -p "$FACTOR_GATEWAY_PROFILE" gateway run` in a separate terminal; it is long-running, not a completion check. Stop waiting after a bounded startup inspection, leave the selected foreground service running in its separate terminal, and report the terminal/process owner and actual status. Do not send a test message automatically; invite me to send one through the chosen channel and verify inbound event, correct profile turn, and reply when authorized. A running process alone is not messaging acceptance.

### 7. Run the selected door and smoke-check

**Mac menu bar:** verify macOS and the Swift toolchain. Inspect the saved `~/Library/Application Support/Factor/company.path`; preserve it unless I selected a different company. Choose the company using the app if needed. Launch the existing shell runner from a separate terminal:

```sh
sh "$FACTOR_REPO/apps/mac/run.sh"
```

This builds and runs the unsigned local tray; it is not the gateway and does not call a model itself. Verify the process and visible tray if the environment permits. Do not mistake a long-running `swift run` for a hung install. On other operating systems, mark the Mac door not applicable.

**Raycast:** if selected, follow `surfaces/raycast/README.md` and add that directory through Raycast's Script Commands settings. It uses the same company path as the Mac door. Do not claim this GUI step completed without observing it.

**Hermes:** verify the installed profile contains the shipped `take-intent` skill. A profile installation does not prove a live model call succeeded.

For a local smoke check, use a disposable company copied with `new-company.sh`, write a sample intent with `scripts/write_intent.py`, and read it with `scripts/intent_card.py`. Do not overwrite the real company's `io/intent.json` to test setup. Run the repository's relevant tests if code or templates were changed; a documentation-only change does not require a live installation.

### 8. Finish with a receipt and a recovery path

Report:

- Fresh install or upgrade; repository path, old/new commit, distribution version and recorded source.
- Company path, profile names and selected doors, without secrets.
- Backup locations and integrity checks; what can actually be restored.
- Doctor, company and room check results, with unresolved issues explicit.
- Gateway owner/topology and observed state; messaging acceptance separately.
- Mac/Raycast/Hermes door checks: verified, pending, or not applicable.
- Preserved settings and any intentional changes; no implied activation of optional capabilities.
- Exact next step for missing facts, authentication or manual interaction.

If a mutation fails, stop dependent steps, keep evidence, and explain the failure. Do not restore everything automatically. Identify the affected files/service and prepare a targeted recovery using the verified backups and old source commit; avoid resetting the whole repository or restoring unrelated profiles. Distinguish source updated, profile installed, process running, and end-to-end verified. Call the install complete only to the level the evidence supports.

## END PROMPT
