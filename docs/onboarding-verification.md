# Bilingual onboarding verification

Source validation date: 27 September 2026. This covers the local implementation and bundled learning library; it does not establish a deployed/installed upgrade or a completed Hermes learning pilot.

## Shipped contract

- English default; French is an explicit choice. Company preference is `preferences.json`; old companies without a file/key use English.
- CLI display override does not change persisted language. Explicit persistence preserves unrelated keys and rejects corrupt, unsupported or symlinked preferences.
- Mac menu uses the same company preference and has a session-only choice before selecting a company. UI labels change; intent keys and room IDs do not.
- Hermes profile instructions consult the preference for explanations and drafts; this is instruction support, not translation of the Hermes application itself. An installed profile must receive the updated instructions before it can use them.
- Seven catalog entries point to two bilingual guides and five French media supports. Seven final binary files include PDF/PPTX exports. They are in the repository and do not require access to the restricted NotebookLM notebook.
- Resource listings have no opener side effect. An explicit selected ID opens a validated local file. No resource selection installs a connector or starts a gateway.

## Evidence

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | 300 tests pass; includes 63 focused onboarding cases |
| `swift test --package-path apps/mac` | 9 tests against the production `FactorMenu` target pass |
| `swift build --package-path apps/mac` | Pass |
| Disposable company with a spaced path | Save FR, read localized steps, use temporary EN override, confirm saved FR unchanged |
| Resource selection | French guide path selected; seven existing resource files; no real intent created |
| Asset integrity | All seven bundled sizes and SHA-256 values match the reviewed originals in `assets/manifest.json` |
| Documentation links | Local targets in README EN/FR, learning library EN/FR and updated setup/resource docs resolve |
| Harvest format | French and English prompts have identical canonical section headings |
| Raycast wrappers | Shell syntax checks pass; existing shared-intent tests pass |
| Diff whitespace | Pass |

Focused tests cover invalid preferences without byte changes, failed writes without false language success, session/default separation, unrelated-key preservation, symlink escapes, absolute/traversal resource paths, malformed manifests, missing/non-file resources, opener failures, language override precedence and interactive selection retention. They call production functions rather than copies of the implementation.

## Native visual check limitation

The current debug binary was packaged and launched as a disposable test app using `FACTOR_COMPANY_PATH_FILE` and a temporary company. The process was observed running. Computer Use timed out attaching to the menu-bar app by both path and bundle ID. No visual toggle/reopen or resource-click acceptance is claimed. The test process was stopped; the user's company selection and preferences were not changed.

Follow-up UI-01: launch `sh apps/mac/run.sh`, inspect English/French labels, select FR, reopen the menu, and open a selected guide. Use a disposable company or the documented absolute `FACTOR_COMPANY_PATH_FILE` development fixture override. Raycast's actual GUI registration and Hermes model response behavior also remain runtime checks rather than claims of this source validation.

## Implementation review

Two isolated external workers returned non-empty patches with successful dispatch status. Dispatcher output selected `cc/claude-sonnet-4-6`; task-specific gateway correlation rows were unavailable, so provider attribution is not treated as verified. Independent integration review found and fixed native persistence/error-handling defects, test copies that did not exercise production code, CLI combined-flag behavior, nested French UI gaps and opener error handling. Dispatch success was not used as acceptance evidence.

No real Hermes profile, gateway, connector, company state or model configuration was modified. The notebook remains restricted. Existing generated-video narration review limits and the learning infographic's pilot-pending caption remain in [the learning library](learning.md).
