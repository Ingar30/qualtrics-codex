# qualtrics-codex

A public starter repository for researchers who want a reproducible local path from Qualtrics to cleaned data, figures, tables, and slides with Codex as the workflow assistant.

The default workflow is deliberately low-friction:

1. Write a simple JSON survey specification.
2. Use Python to create or connect to a Qualtrics survey.
3. Export responses as CSV or SPSS/SAV.
4. Analyze with lab-style Stata cleaning/figure scripts when available.
5. Fall back to Python analysis when Stata is missing or broken.
6. Build Beamer slides when LaTeX is available.
7. Fall back to the built-in Python slide renderer when LaTeX is missing or broken.

The default assumes many economists already use Stata and LaTeX/Beamer. The repository still keeps no-install fallbacks: Python analysis, Markdown slide content, a small Python renderer, custom CSS, and optional browser-based PDF export.

The public GitHub Pages site is built only from synthetic fixture data. Live Qualtrics exports are intended to run locally on your machine with credentials stored outside the repository.

## Intended Codex Loop

The main use case is conversational:

1. Ask Codex for a survey, either with exact questions or a broad research idea.
2. Codex creates the survey spec, analysis scripts, and slides.
3. Codex asks or infers whether you want a synthetic local test, a live draft/test link, or an export of real responses.
4. Codex generates or downloads responses.
5. Codex cleans the data in Stata when available, otherwise Python.
6. Codex generates figures and tables.
7. Codex compiles Beamer slides when available, otherwise native HTML slides.

A canonical full-loop prompt is:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Because that prompt asks Codex to create a survey and generate responses on Qualtrics, Codex should treat it as a live API workflow: first verify local credentials without printing them, then ask before creating the draft survey, submitting synthetic responses, or exporting responses. For a no-credentials smoke test, ask Codex to generate the synthetic responses locally instead.

The repo also includes granular Codex skills for the main pieces of the loop: survey creation, synthetic responses, SAV export, Stata cleaning, Stata figures, Beamer slides, reusable links, and slide review. The top-level `qualtrics-survey-loop` skill routes among them.

See `docs/intended-codex-loop.md`, `prompts/full-loop-survey.md`, and `prompts/discrimination-beliefs-example.md`.

## Quick Start

Install prerequisites:

- Python 3.10 or newer.

Create and activate a Python environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install Python packages:

```bash
python -m pip install -r requirements.txt
```

Windows users can use the setup helper:

```powershell
.\scripts\setup.ps1
```

If virtual environment creation fails and leaves a partial `.venv/`, see `docs/setup-troubleshooting.md`. For a quick non-venv fallback:

```powershell
.\scripts\setup.ps1 -User
```

## Use This Repo With Codex

Clone the starter repo, enter the folder, and open it in Codex:

```bash
git clone https://github.com/Ingar30/qualtrics-codex.git
cd qualtrics-codex
codex
```

If you launch Codex from another folder, point it at the repo:

```bash
codex --cd path/to/qualtrics-codex
```

Then paste the starter prompt from:

```text
prompts/start-with-codex.md
```

That prompt tells Codex to inspect the repository, scaffold a new survey workflow, generate synthetic responses, run the local smoke test, and avoid live Qualtrics calls until you explicitly ask.

If you want Codex to remember local workflow preferences before scaffolding, start with:

```text
prompts/configure-local-preferences.md
```

Those preferences should be written to ignored `AGENTS.override.md`, never to committed docs. The default is Stata-first when available with Python fallback, Beamer-first with native fallback, local synthetic smoke tests before live Qualtrics calls, SAV/SPSS exports for Stata workflows, and CSV exports for Python workflows.

You do not need Qualtrics API keys for the synthetic smoke test. Before asking Codex to create surveys, list surveys, or export real responses, store your keys outside the repository. See `docs/local-qualtrics-secrets.md`.

If you prefer to ask Codex in plain language instead of running commands yourself, see:

```text
docs/codex-prompt-alternatives.md
```

You can also start from the worked example:

```text
prompts/discrimination-beliefs-example.md
```

## Run The Local Smoke Test

This does not call the Qualtrics API.

```bash
python scripts/generate_synthetic_responses.py --survey-key repo_smoke_test --output build/fixtures/repo_smoke_test_responses.csv
python scripts/run_analysis.py --survey-key repo_smoke_test --input build/fixtures/repo_smoke_test_responses.csv
python scripts/build_slides.py --survey-key repo_smoke_test
```

If Beamer compiles, the PDF is written to:

```text
build/slides/repo_smoke_test/slides.pdf
```

If LaTeX is missing or compilation fails, the script falls back to the native Python slide deck:

```text
build/slides/repo_smoke_test/slides.html
```

The fallback also exports a PDF when Chrome, Edge, or Chromium is already installed. To force the Python path:

```bash
python scripts/run_analysis.py --survey-key repo_smoke_test --input build/fixtures/repo_smoke_test_responses.csv --mode python
python scripts/build_slides.py --survey-key repo_smoke_test --mode python
```

When comparing Beamer and native PDF output in the same folder, write the native PDF to a separate file:

```bash
python scripts/render_slides.py --survey-key repo_smoke_test --pdf --pdf-output build/slides/repo_smoke_test/slides-native.pdf
```

The repository also keeps a committed synthetic fixture at `tests/fixtures/repo_smoke_test_responses.csv` for unit tests. For new local checks, prefer generating fresh synthetic responses into `build/fixtures/` so test data is clearly disposable.

## Live Qualtrics Test Loop

Live API actions are local/manual by default. Store credentials outside the repo, load them in your shell, and run:

```bash
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key discrimination_beliefs_demo --survey-name "Discrimination Beliefs Demo" --spec-file code/discrimination_beliefs_demo/survey_spec.json
python scripts/qualtrics_workflow.py get-link --survey-key discrimination_beliefs_demo --write-slide-inputs
python scripts/generate_synthetic_responses.py --survey-key discrimination_beliefs_demo --output build/fixtures/discrimination_beliefs_demo_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key discrimination_beliefs_demo --input build/fixtures/discrimination_beliefs_demo_responses.csv --limit 1
python scripts/qualtrics_workflow.py export-responses --survey-key discrimination_beliefs_demo --format csv
python scripts/run_analysis.py --survey-key discrimination_beliefs_demo
python scripts/build_slides.py --survey-key discrimination_beliefs_demo
```

After inspecting the one-response export locally, submit the remaining rows without duplicating the first row:

```bash
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key discrimination_beliefs_demo --input build/fixtures/discrimination_beliefs_demo_responses.csv --resume
python scripts/qualtrics_workflow.py export-responses --survey-key discrimination_beliefs_demo --format csv
python scripts/run_analysis.py --survey-key discrimination_beliefs_demo
python scripts/build_slides.py --survey-key discrimination_beliefs_demo
```

If you explicitly want one command for the synthetic response submission, use `--smoke-then-rest`. The scripts do not print survey IDs, response IDs, reusable links, tokens, or raw response contents by default.

`get-link --write-slide-inputs` writes the reusable link into ignored local slide input files so local Beamer/native slides can include it without printing it in the terminal. Do not commit or publish those local link inputs by default.

## Analysis Workflow

The base repo optimizes for a Stata-first workflow with a Python fallback:

- For the lab-style economist path, write Stata cleaning in `code/<survey_key>/cleaning/run.do` and Stata figures in `code/<survey_key>/figures/run.do`.
- For the compact fallback path, write Stata analysis in `code/<survey_key>/analysis/run.do`.
- Keep a Python fallback in `code/<survey_key>/analysis/run.py`.
- Run `scripts/run_analysis.py`.
- Let Codex diagnose Stata locally when it can.
- Fall back to Python analysis without installing Stata.
- Use SPSS/SAV exports for Stata workflows and CSV exports for Python workflows.

Both analysis paths write the same reproducible outputs:

```text
data/<survey_key>/processed/clean.csv
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/*.pdf
slides/<survey_key>/inputs/*.png
```

Figure PDFs are the preferred Beamer inputs because they keep charts sharp in the final slide PDF. PNGs are kept for the Python HTML fallback.

Before real Qualtrics responses exist, use:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
```

This lets Codex validate cleaning, figures, tables, and slides without creating a survey, calling the API, or touching private data.

For SPSS/SAV exports and lab-style Stata scripts:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

For Python analysis of a live export:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key> --mode python
```

Windows users can use the compatibility wrappers:

```powershell
.\scripts\load-project.ps1 -RequireQualtrics
.\scripts\run-survey-pipeline.ps1 -SurveyKey <survey_key> -SurveyName "<survey name>" -Format spss
.\scripts\run-stata-analysis.ps1 -SurveyKey <survey_key>
.\scripts\build-slides.ps1 -SurveyKey <survey_key>
```

If Stata is installed but not discoverable, set `STATA_EXE`, for example:

```powershell
$env:STATA_EXE = "C:\Program Files\Stata19\StataMP-64.exe"
```

## Slide Workflow

The base repo optimizes for a Beamer-first workflow with a Python escape hatch:

- Write the preferred deck in `slides/<survey_key>/main.tex`.
- Write slides in `slides/<survey_key>/slides.md`.
- Run `scripts/build_slides.py`.
- Let Codex diagnose LaTeX locally when it can.
- Fall back to Python slides without installing any slide software.

Both slide paths read generated tables and figures from `slides/<survey_key>/inputs/`. The first run should still work without Stata, LaTeX, Quarto, R, Node, Jinja2, or YAML.

## Synthetic Response Weights

Survey specs can make local synthetic data less uniform with `synthetic_weights` on multiple-choice questions. Use either a list matching `choices`:

```json
"synthetic_weights": [0.05, 0.12, 0.18, 0.42, 0.23]
```

or an object keyed by choice label:

```json
"synthetic_weights": {
  "Somewhat common": 0.42,
  "Very common": 0.23
}
```

Missing object keys get zero weight. Weights must be nonnegative and sum above zero.

## Run Tests

Normal pytest works:

```bash
python -m pytest
```

In restricted environments, the PowerShell helper keeps pytest temp/cache directories under `build/`:

```powershell
.\scripts\run_tests.ps1
```

## Configure Local Qualtrics Secrets

Do not put Qualtrics credentials in this repository. Store them outside the repo and load them only before live API calls. The synthetic smoke test, unit tests, and GitHub Pages demo do not need these keys.

Detailed setup notes live in:

```text
docs/local-qualtrics-secrets.md
```

Qualtrics' API overview explains that API tokens live under Account Settings, in the Qualtrics IDs area:

```text
https://www.qualtrics.com/support/integrations/api-integration/overview/
```

Recommended Windows PowerShell file location:

```text
$HOME\.secrets\qualtrics.env.ps1
```

Example contents:

```powershell
$env:QUALTRICS_DATACENTER = "your_datacenter"
$env:QUALTRICS_API_TOKEN = "your_token"
$env:QUALTRICS_PUBLIC_HOST = "yourbrand.qualtrics.com"
```

Load it before live API calls:

```powershell
. $HOME\.secrets\qualtrics.env.ps1
```

Recommended macOS/Linux shell file location:

```text
$HOME/.secrets/qualtrics.env
```

Example contents:

```bash
export QUALTRICS_DATACENTER="your_datacenter"
export QUALTRICS_API_TOKEN="your_token"
export QUALTRICS_PUBLIC_HOST="yourbrand.qualtrics.com"
```

Load it before live API calls:

```bash
source "$HOME/.secrets/qualtrics.env"
```

Required environment variables:

```text
QUALTRICS_API_TOKEN
QUALTRICS_DATACENTER
```

Optional:

```text
QUALTRICS_PUBLIC_HOST
```

Never commit `.env`, `.secrets/`, API tokens, raw exports, or real response data.

## Create A Survey

The example survey spec lives at:

```text
code/repo_smoke_test/survey_spec.json
```

Create the survey as a draft:

```bash
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key repo_smoke_test --survey-name "Repository Smoke Test Survey" --spec-file code/repo_smoke_test/survey_spec.json
```

Activate immediately only when you intend to collect responses:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key repo_smoke_test --survey-name "Repository Smoke Test Survey" --spec-file code/repo_smoke_test/survey_spec.json --activate
```

Get the reusable anonymous link:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key repo_smoke_test --write-slide-inputs
```

By default, the link is saved to ignored local metadata without printing it. `--write-slide-inputs` also saves ignored local inputs for slide decks. Add `--show-private-link` only when you need to see it in your local terminal.

Download responses as CSV:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key repo_smoke_test --format csv
```

Then analyze the newest downloaded CSV:

```bash
python scripts/run_analysis.py --survey-key repo_smoke_test
python scripts/build_slides.py --survey-key repo_smoke_test
```

Qualtrics CSV exports often include two metadata rows after the header. The included smoke-test analysis filters those rows when `ResponseId` is present by keeping response IDs that start with `R_`.

## GitHub Pages Demo

The Pages site is a public demo built from generated synthetic responses. It publishes only synthetic artifacts:

```text
site/index.html
site/walkthrough.html
site/artifacts/smoke-slides.pdf
site/artifacts/smoke-slides.html
site/artifacts/smoke-figures.zip
site/artifacts/smoke-tables.zip
site/artifacts/discrimination-beliefs-demo-slides.pdf
site/artifacts/discrimination-beliefs-demo-slides.html
site/artifacts/discrimination-beliefs-demo-figures.zip
site/artifacts/discrimination-beliefs-demo-tables.zip
```

Build it locally:

```bash
python scripts/build_site.py --output-dir site
```

The Pages workflow in `.github/workflows/pages.yml` builds the same site on pushes to `main`. It does not use Qualtrics secrets and does not call the live Qualtrics API.

Expected public URL after publishing under Ingar30:

```text
https://ingar30.github.io/qualtrics-codex/
```

## Scaffold A New Project With Codex

Use the starter prompt in:

```text
prompts/start-with-codex.md
```

For a shorter scaffold-only version, use:

```text
prompts/scaffold-workflow.md
```

For an optional first-run preference conversation, use:

```text
prompts/configure-local-preferences.md
```

It asks Codex to create a new `code/<survey_key>/` folder, lab-style Stata cleaning/figure scripts or a compact Stata analysis script, a Python analysis fallback, a Beamer deck, a Python-native Markdown fallback deck, and safe ignored output folders.

For the complete survey-to-responses-to-slides loop, use:

```text
prompts/full-loop-survey.md
```

For a concrete example survey about beliefs around discrimination, use:

```text
prompts/discrimination-beliefs-example.md
```

For a final repo validation pass before publishing or sharing, use:

```text
prompts/final-validation-goal.md
```

## Supporting Docs

- Stata/SPSS workflow: `docs/stata-extension.md`
- Beamer/Python slide workflow: `docs/latex-extension.md`
- Intended Codex loop: `docs/intended-codex-loop.md`
- Setup troubleshooting: `docs/setup-troubleshooting.md`
- Local Qualtrics secrets: `docs/local-qualtrics-secrets.md`
- Codex prompt alternatives: `docs/codex-prompt-alternatives.md`
- Reproducibility notes: `docs/reproducibility.md`
- Local preference prompt: `prompts/configure-local-preferences.md`

These document the traditional economist stack and the fallback contract. The base repo should still produce slides even when Stata, LaTeX, Quarto, R, Node, Jinja2, and YAML are unavailable.

## Safety Defaults

- Raw exports stay under `data/<survey_key>/raw/` and are ignored by git.
- Processed data stays under `data/<survey_key>/processed/` and is ignored by git.
- Generated slide inputs and rendered decks are ignored by git.
- The generated `site/` directory is ignored by git and rebuilt by GitHub Actions from synthetic data.
- Live API actions require explicit commands and environment variables.
- API tokens are never printed intentionally by the scripts.
- New `code/<survey_key>/` and `slides/<survey_key>/` folders are ignored by default unless explicitly allowlisted as public demos.


For guarded local live validation, see `docs/live-validation.md` or dry-run the sequence first:

```powershell
python scripts/run_live_validation.py --survey-key "<survey_key>" --survey-name "<survey name>" --spec-file "code/<survey_key>/survey_spec.json" --n 100 --dry-run --i-understand-this-calls-qualtrics
```
