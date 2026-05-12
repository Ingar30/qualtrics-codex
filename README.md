# qualtrics-codex

A public starter repository for teaching a reproducible Qualtrics-to-analysis-to-slides workflow with Codex as the assistant.

The core idea is simple: a researcher describes a survey or research topic in Codex, and Codex helps build the workflow around it. The workflow can create a Qualtrics test survey, submit synthetic responses to that survey for a live demo, export the responses, clean the data, make figures and tables, and compile a short PDF/HTML slide deck.

## What This Repo Teaches

- How to ask Codex to turn a research idea into a small Qualtrics-ready survey.
- How to keep live Qualtrics actions explicit, local, and credential-protected.
- How to use synthetic responses as a teaching/demo aid, with the normal live demo submitting them through Qualtrics rather than treating local CSVs as the main object.
- How to move from exported Qualtrics data to cleaned data, figures, tables, and slides.
- How to keep Stata and Beamer as the preferred economist-style path while retaining Python and native HTML fallbacks.

Public GitHub Pages artifacts are built from synthetic fixture data only. Real exports, raw rows, metadata, reusable links, survey IDs, response IDs, and credentials stay local by default.

## Start With Codex

Clone the repo, install the local dependencies, and open Codex in the project folder:

```bash
git clone https://github.com/Ingar30/qualtrics-codex.git
cd qualtrics-codex
```

On Windows PowerShell, the setup helper creates the environment and installs the Python requirements:

```powershell
.\scripts\setup.ps1
codex
```

If you open Codex somewhere else, point it at this repo:

```bash
codex --cd path/to/qualtrics-codex
```

First, paste this opening prompt into Codex. It tells Codex to inspect the local environment, report what is missing without printing secrets, and then ask the necessary follow-up questions:

```text
Open prompts/configure-local-preferences.md and follow it as instructions for this Codex session. Do not summarize it.

First inspect this repository and the local environment without changing files or calling Qualtrics. Check Python and dependencies, whether Stata is discoverable through STATA_EXE, PATH, or common install paths, whether LaTeX/Beamer tools are available, and whether QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values.

If Stata is not found, ask me whether I have Stata installed and where the executable is. On Windows it often looks like C:\Program Files\Stata19\StataMP-64.exe, and the path can be supplied with STATA_EXE. If LaTeX/Beamer is not found, ask whether to continue with native HTML slides or help configure LaTeX.

If Qualtrics secrets are not found, tell me where to create or load the local secrets file: docs/local-qualtrics-secrets.md, $HOME\.secrets\qualtrics.env.ps1 on Windows, or $HOME/.secrets/qualtrics.env on macOS/Linux. Do not ask me to paste token values into Codex.

Then ask only the follow-up questions needed to set my local workflow preferences: Stata-first vs Python-only, SPSS/SAV vs CSV exports, Beamer vs native HTML slides, live Qualtrics behavior for the main demo, and the public/private boundary. Save my answers in ignored AGENTS.override.md without secrets, survey IDs, response IDs, or reusable links.
```

Short plain-language version:

```text
Ask me about my local preferences for this Qualtrics workflow before we build anything. First inspect Python, Stata, LaTeX, and Qualtrics environment-variable status without printing secrets. If Stata, LaTeX, or Qualtrics secrets are missing, tell me where to configure them or which fallback to use. Then ask the needed follow-up questions and save my answers in ignored AGENTS.override.md without secrets.
```

If you skip this step, the repo defaults to Stata and Beamer when available, with Python and native slides as fallbacks. If Stata is installed but Codex cannot find it, point the session at the executable with `STATA_EXE`. On Windows that usually looks like:

```powershell
$env:STATA_EXE = "C:\Program Files\Stata19\StataMP-64.exe"
```

See `docs/setup-troubleshooting.md` and `docs/stata-extension.md` for the Stata lookup and fallback details.

## Main Live Teaching Demo

After local preferences are set, use plain language and let Codex choose the scripts and fallbacks:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should interpret that as a live API workflow. It should verify credentials without printing them, ask before creating the draft survey, ask before submitting synthetic responses to Qualtrics, ask before exporting responses, and keep private identifiers and reusable links out of the public repo.

More prompt variants live in `docs/codex-prompt-alternatives.md`, and the full conversational loop is documented in `docs/intended-codex-loop.md`.

## What Codex Builds

For a new survey workflow, Codex should create the small reusable pieces that make the process teachable:

- `code/<survey_key>/survey_spec.json` for the survey structure.
- Survey-specific cleaning and figure code under `code/<survey_key>/`.
- Slide sources under `slides/<survey_key>/`.
- Generated tables and figures under `slides/<survey_key>/inputs/`.
- Local raw exports, processed data, metadata, and rendered outputs in ignored folders.

The preferred analysis path is Stata with SPSS/SAV exports when Stata is available. The fallback is Python analysis with CSV exports. The preferred slide path is Beamer when LaTeX is available. The fallback is the native Markdown/HTML/PDF renderer. Codex should diagnose local tool availability and use the simplest working path.

## Secrets And Public Safety

Do not put Qualtrics credentials in this repository. Store them outside the repo and load them only before live API calls. The expected local variables are:

```text
QUALTRICS_API_TOKEN
QUALTRICS_DATACENTER
QUALTRICS_PUBLIC_HOST
```

`QUALTRICS_PUBLIC_HOST` is optional. Setup details are in `docs/local-qualtrics-secrets.md`.

The safe defaults are:

- live Qualtrics mutations and exports require explicit user approval;
- tokens are never intentionally printed;
- local survey metadata and reusable links are ignored by git;
- raw exports and processed real data are ignored by git;
- new `code/<survey_key>/` and `slides/<survey_key>/` folders stay private unless explicitly promoted;
- GitHub Pages and CI do not call Qualtrics and do not need Qualtrics secrets.

## Where Details Live

- Start prompt: `prompts/start-with-codex.md`
- Full live-loop prompt: `prompts/full-loop-survey.md`
- Worked example prompt: `prompts/discrimination-beliefs-example.md`
- Local preference prompt: `prompts/configure-local-preferences.md`
- Prompt cookbook: `docs/codex-prompt-alternatives.md`
- Intended Codex loop and command reference: `docs/intended-codex-loop.md`
- Local Qualtrics secrets: `docs/local-qualtrics-secrets.md`
- Setup troubleshooting: `docs/setup-troubleshooting.md`
- Stata/SPSS notes: `docs/stata-extension.md`
- Beamer/native slide notes: `docs/latex-extension.md`
- Public validation boundary: `docs/live-validation.md`
- Reproducibility contract: `docs/reproducibility.md`

For final local validation before sharing changes, ask Codex to use `prompts/final-validation-goal.md`. For GitHub Pages, the workflow rebuilds the public demo site on pushes to `main` without Qualtrics secrets or live API calls.
