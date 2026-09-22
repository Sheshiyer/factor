# Mac menu

The first build is unsigned and local.

The app does not call a model. It writes an intent.

## Run

Set the company folder, then run the menu from this directory.

Write one absolute path into `~/Library/Application Support/Factor/company.path`, or leave that file missing and choose the folder in the menu. The menu keeps one company folder. Quit does not delete it.

```bash
apps/mac/run.sh
```

That sets `FACTOR_ROOT` to this repository and opens the tray. The tray is a filled circle and the company name. There is no Dock icon.

`FACTOR_ROOT` is the Factor repository. The menu runs `python3` on `$FACTOR_ROOT/scripts/write_intent.py`. Set `FACTOR_WRITE_INTENT` to that script if the repository root is not `FACTOR_ROOT`.

The field is the job. The room is one of content, numbers, growth, ads, partners, or money. This door is `mac`. Rollback is shown only when `scripts/rollback.py` is already there.
