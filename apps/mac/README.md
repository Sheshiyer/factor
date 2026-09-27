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

## Language and learning resources

English is default. The EN/FR selector updates the visible labels immediately. With a company selected, the choice is stored in that company's `preferences.json` and shared with CLI onboarding and Factor's Hermes instructions. Without a company it is session-only. Existing company text and canonical intent IDs remain unchanged.

The learning resources menu is available before completing onboarding. It reads `docs/resources.json` from the framework checkout and opens a selected local guide, deck, video or infographic. Guides have English and French versions; media currently are French-only. A missing checkout or file produces a notice, not an invented link. The Mac app does not install tools or call a model when opening resources.

[English learning library](../../docs/learning.md) · [Ressources en français](../../docs/learning.fr.md).

For isolated development checks, `FACTOR_COMPANY_PATH_FILE` may point to an absolute test-only company selection file. It leaves the normal `~/Library/Application Support/Factor/company.path` unchanged. [Verification and remaining native visual check](../../docs/onboarding-verification.md).
