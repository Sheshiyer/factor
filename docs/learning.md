# Learn Factor

**English** · [Français](learning.fr.md)

Start with the framework guide, then use the operator guide for your first company and task. English is the default interface language; French is an explicit choice. These resources explain the framework, the separate company workspace, and the Hermes learning pilot that still needs validation.

| What you need | English | Français |
|---|---|---|
| Understand the architecture | [Framework guide](ecosystem/2026-09-27/ecosystem.en.md) | [Guide du framework](ecosystem/2026-09-27/ecosystem.fr.md) |
| Set up and do the first job | [Operator guide](ecosystem/2026-09-27/playbook.en.md) | [Guide opérationnel](ecosystem/2026-09-27/playbook.fr.md) |
| Run installation or upgrade with an assistant | [Copyable install prompt](../prompt-install.md) | Use the same prompt and request replies in French |

## Watch, present, or explain

The visual assets currently available are **in French**. Choosing English changes the interface and guide selection; it does not translate an existing video or slide deck.

| Asset | Open or download |
|---|---|
| Framework overview — 8 slides | [PDF](assets/fr/framework-slides-v2.pdf) · [PowerPoint](assets/fr/framework-slides-v2.pptx) |
| Operating workflow — 8 slides | [PDF](assets/fr/operations-slides-v2.pdf) · [PowerPoint](assets/fr/operations-slides-v2.pptx) |
| Video overview — 5 min 10 sec | [MP4](assets/fr/overview-video.mp4) |
| Architecture at a glance | [PNG](assets/fr/architecture-infographic-v2.png) |
| Learning from verified work | [PNG](assets/fr/learning-infographic-v2.png) |

![Factor architecture, in French](assets/fr/architecture-infographic-v2.png)

The learning infographic describes a **proposed protocol; the Hermes pilot remains to be validated**. The decks and infographics were visually reviewed. The video passed full decoding and sampled visual review; its narration was not independently reviewed. Some minor labels remain imperfect. [Review details](ecosystem/2026-09-27/media-fr/verification.md).

Files are bundled for offline access. [NotebookLM](https://notebooklm.google.com/notebook/ed5305d5-9bca-4a00-b2a8-5d2f811c1222) is the source notebook and requires access; opening local files does not require a NotebookLM account. [Asset provenance and hashes](assets/manifest.json).

## Find these resources during onboarding

```sh
# English by default; listing never opens an application.
python3 scripts/onboard.py --resources
python3 scripts/onboard.py --language fr --resources

# Structured resource list for a coding assistant.
python3 scripts/onboard.py --language fr --resources --json

# Open just the selected guide, using the default desktop application.
python3 scripts/onboard.py --language fr --open-resource framework-guide
```

The interactive onboarding menu offers language and resource choices. The Mac menu offers an EN/FR selector and a learning resources menu. These are user-triggered actions: reading a list does not start a browser, install a tool, or call a model.

## Choose a language

```sh
# Change the interface for this invocation only.
python3 scripts/onboard.py --language fr --steps

# Remember French for this company.
python3 scripts/onboard.py --company /absolute/path/to/company --set-language fr

# Return the company to English.
python3 scripts/onboard.py --company /absolute/path/to/company --set-language en
```

The company preference is `preferences.json`, with `"language": "en"` or `"fr"`. Old companies without the file use English. An explicit `--language` takes precedence for one CLI invocation without changing the saved choice. The Mac toggle shares the company preference. Before selecting a company it is session-only.

Factor's Hermes instructions read this preference for explanations and drafts unless the task or an approved brand requirement explicitly specifies another output language. Existing company text, quotes, source material and catalog descriptions are not automatically translated. Room IDs, file names, JSON keys and harvest section headings remain stable. Invalid preference files are reported rather than overwritten.

For Raycast, the English command remains available, with a separate French command because Script Command labels are static. Use the Mac or onboarding language selector to persist the company's preferred response language. [Raycast setup](../surfaces/raycast/README.md).

[Implementation verification and runtime limits](onboarding-verification.md).
