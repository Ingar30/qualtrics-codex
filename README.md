# qualtrics-codex

A public starter repository for teaching a Qualtrics-to-analysis-to-slides workflow with Codex as the assistant.

The core idea is simple: Codex helps create a Qualtrics test survey, generate synthetic responses for that survey, submit those responses through Qualtrics before the survey is launched to human subjects, export the generated responses, analyze the data, and compile a short PDF/HTML slide deck.

Public GitHub Pages artifacts are built from synthetic fixture data only. Real exports, raw rows, metadata, reusable links, survey IDs, response IDs, and credentials stay local by default.

## 1. Get Qualtrics API Access

Qualtrics' official API overview is here:

https://www.qualtrics.com/support/integrations/api-integration/overview/

To use the live teaching demo, your Qualtrics account needs API access. In Qualtrics, go to:

```text
User settings icon -> Account Settings -> Qualtrics IDs -> API -> Generate Token
```

Qualtrics notes that the account must have the **Access API** permission enabled. If you already have an API token, do not generate a new one casually: replacing a token can break existing tools that use the old token.

You need two required values:

```text
QUALTRICS_DATACENTER
QUALTRICS_API_TOKEN
```

`QUALTRICS_DATACENTER` is the datacenter part of the API URL. If your API base URL looks like this:

```text
https://yourdatacenterid.qualtrics.com/API/v3
```

then use:

```text
QUALTRICS_DATACENTER=yourdatacenterid
```

Do not include `https://`, `.qualtrics.com`, or `/API/v3` in `QUALTRICS_DATACENTER`.

## 2. Save Secrets Locally

Do not put API tokens in this repository and do not paste them into Codex.

On Windows PowerShell, create a secrets file outside the repo:

```powershell
New-Item -ItemType Directory -Force $HOME\.secrets
notepad $HOME\.secrets\qualtrics.env.ps1
```

Put this in `$HOME\.secrets\qualtrics.env.ps1`:

```powershell
$env:QUALTRICS_DATACENTER = "your_datacenter"
$env:QUALTRICS_API_TOKEN = "your_token"
$env:QUALTRICS_PUBLIC_HOST = "yourbrand.qualtrics.com"
```

`QUALTRICS_PUBLIC_HOST` is optional. Use it when your respondent-facing survey links use a branded host that differs from the API datacenter host.

Load the file before opening Codex for a live demo:

```powershell
. $HOME\.secrets\qualtrics.env.ps1
```

macOS/Linux examples are in `docs/local-qualtrics-secrets.md`.

## 3. Clone And Install

Clone the repo, install the Python requirements, and open Codex in the project folder:

```powershell
git clone https://github.com/Ingar30/qualtrics-codex.git
cd qualtrics-codex
.\scripts\setup.ps1
. $HOME\.secrets\qualtrics.env.ps1
codex
```

If you open Codex somewhere else, point it at this repo:

```bash
codex --cd path/to/qualtrics-codex
```

## 4. First Codex Prompt

Paste this opening prompt into Codex. It tells Codex to inspect the local environment, report what is missing without printing secrets, and ask the necessary follow-up questions:

```text
Open prompts/configure-local-preferences.md and follow it as instructions for this Codex session. Do not summarize it.

First inspect this repository and the local environment without changing files or calling Qualtrics. Check Python and dependencies, whether Stata is discoverable through STATA_EXE, PATH, or common install paths, whether LaTeX/Beamer tools are available, and whether QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values.

If Stata is not found, ask me whether I have Stata installed and where the executable is. On Windows it often looks like C:\Program Files\Stata19\StataMP-64.exe, and the path can be supplied with STATA_EXE. If LaTeX/Beamer is not found, ask whether to continue with native HTML slides or help configure LaTeX.

If Qualtrics secrets are not found, tell me where to create or load the local secrets file: docs/local-qualtrics-secrets.md, $HOME\.secrets\qualtrics.env.ps1 on Windows, or $HOME/.secrets/qualtrics.env on macOS/Linux. Do not ask me to paste token values into Codex.

Then ask only the follow-up questions needed to set my local workflow preferences: Stata-first vs Python-only, SPSS/SAV vs CSV exports, Beamer vs native HTML slides, live Qualtrics behavior for the main demo, and the public/private boundary. Save my answers in ignored AGENTS.override.md without secrets, survey IDs, response IDs, or reusable links.
```

If Stata is installed but Codex cannot find it, point the session at the executable with `STATA_EXE`:

```powershell
$env:STATA_EXE = "C:\Program Files\Stata19\StataMP-64.exe"
```

## 5. Main Live Teaching Demo

After local preferences are set, paste the canonical prompt:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics to test the survey before it is launched to human subjects, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should treat this as a live API workflow. It should verify credentials without printing them, ask before creating the draft survey, ask before submitting synthetic responses to Qualtrics, ask before exporting responses, and keep private identifiers and reusable links out of the public repo.

The worked prompt lives in `prompts/discrimination-beliefs-example.md`. Short prompt variants live in `docs/codex-prompt-alternatives.md`.

## What Codex Builds

For a new survey workflow, Codex should create the small reusable pieces that make the process teachable:

- `code/<survey_key>/survey_spec.json` for the survey structure.
- Survey-specific cleaning and figure code under `code/<survey_key>/`.
- Slide sources under `slides/<survey_key>/`.
- Generated tables and figures under `slides/<survey_key>/inputs/`.
- Local raw exports, processed data, metadata, and rendered outputs in ignored folders.

The preferred analysis path is Stata with SPSS/SAV exports when Stata is available. The fallback is Python analysis with CSV exports. The preferred slide path is Beamer when LaTeX is available. The fallback is the native Markdown/HTML/PDF renderer.

## Safety Boundary

The safe defaults are:

- live Qualtrics mutations and exports require explicit user approval;
- tokens are never intentionally printed;
- local survey metadata and reusable links are ignored by git;
- raw exports and processed real data are ignored by git;
- new `code/<survey_key>/` and `slides/<survey_key>/` folders stay private unless explicitly promoted;
- GitHub Pages and CI do not call Qualtrics and do not need Qualtrics secrets.

## Where Details Live

- Worked example prompt: `prompts/discrimination-beliefs-example.md`
- Local preference prompt: `prompts/configure-local-preferences.md`
- Prompt alternatives: `docs/codex-prompt-alternatives.md`
- Main Codex loop: `docs/intended-codex-loop.md`
- Local Qualtrics secrets: `docs/local-qualtrics-secrets.md`
- Setup troubleshooting: `docs/setup-troubleshooting.md`
- Stata/SPSS notes: `docs/stata-extension.md`
- Beamer/native slide notes: `docs/latex-extension.md`
- Public validation boundary: `docs/live-validation.md`
- Reproducibility contract: `docs/reproducibility.md`

For final local validation before sharing changes, ask Codex to use `prompts/final-validation-goal.md`. For GitHub Pages, the workflow rebuilds the public demo site on pushes to `main` without Qualtrics secrets or live API calls.
