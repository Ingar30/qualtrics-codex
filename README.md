# qualtrics-codex

A public starter repository for researchers who want a reproducible local path from Qualtrics to cleaned data, figures, tables, and slides with Codex as the workflow assistant.

The default workflow is deliberately low-friction:

1. Write a simple JSON survey specification.
2. Use Python to create or connect to a Qualtrics survey.
3. Export responses as CSV.
4. Analyze the CSV with Stata when available.
5. Fall back to Python analysis when Stata is missing or broken.
6. Build Beamer slides when LaTeX is available.
7. Fall back to the built-in Python slide renderer when LaTeX is missing or broken.

The default assumes many economists already use Stata and LaTeX/Beamer. The repository still keeps no-install fallbacks: Python analysis, Markdown slide content, a small Python renderer, custom CSS, and optional browser-based PDF export.

The public GitHub Pages site is built only from synthetic fixture data. Live Qualtrics exports are intended to run locally on your machine with credentials stored outside the repository.

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

## Run The Local Smoke Test

This does not call the Qualtrics API.

```bash
python scripts/run_analysis.py --survey-key repo_smoke_test --input tests/fixtures/repo_smoke_test_responses.csv
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
python scripts/run_analysis.py --survey-key repo_smoke_test --input tests/fixtures/repo_smoke_test_responses.csv --mode python
python scripts/build_slides.py --survey-key repo_smoke_test --mode python
```

## Analysis Workflow

The base repo optimizes for a Stata-first workflow with a Python fallback:

- Write the preferred analysis in `code/<survey_key>/analysis/run.do`.
- Keep a Python fallback in `code/<survey_key>/analysis/run.py`.
- Run `scripts/run_analysis.py`.
- Let Codex diagnose Stata locally when it can.
- Fall back to Python analysis without installing Stata.

Both analysis paths write the same reproducible outputs:

```text
data/<survey_key>/processed/clean.csv
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/*.pdf
slides/<survey_key>/inputs/*.png
```

Figure PDFs are the preferred Beamer inputs because they keep charts sharp in the final slide PDF. PNGs are kept for the Python HTML fallback.

## Slide Workflow

The base repo optimizes for a Beamer-first workflow with a Python escape hatch:

- Write the preferred deck in `slides/<survey_key>/main.tex`.
- Write slides in `slides/<survey_key>/slides.md`.
- Run `scripts/build_slides.py`.
- Let Codex diagnose LaTeX locally when it can.
- Fall back to Python slides without installing any slide software.

Both slide paths read generated tables and figures from `slides/<survey_key>/inputs/`. The first run should still work without Stata, LaTeX, Quarto, R, Node, Jinja2, or YAML.

## Configure Local Qualtrics Secrets

Do not put Qualtrics credentials in this repository. Store them outside the repo.

Recommended Windows PowerShell file:

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
python scripts/qualtrics_workflow.py create-survey --survey-key repo_smoke_test --survey-name "Repository Smoke Test Survey" --spec-file code/repo_smoke_test/survey_spec.json
```

Activate immediately only when you intend to collect responses:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key repo_smoke_test --survey-name "Repository Smoke Test Survey" --spec-file code/repo_smoke_test/survey_spec.json --activate
```

Get the reusable anonymous link:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key repo_smoke_test
```

Download responses as CSV:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key repo_smoke_test --format csv
```

Then analyze the newest downloaded CSV:

```bash
python scripts/run_analysis.py --survey-key repo_smoke_test
python scripts/build_slides.py --survey-key repo_smoke_test
```

## GitHub Pages Demo

The Pages site is a public demo built from `tests/fixtures/repo_smoke_test_responses.csv`. It publishes only synthetic artifacts:

```text
site/index.html
site/walkthrough.html
site/artifacts/slides.pdf
site/artifacts/slides.html
site/artifacts/figures.zip
site/artifacts/tables.zip
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

Use the prompt in:

```text
prompts/scaffold-workflow.md
```

It asks Codex to create a new `code/<survey_key>/` folder, a Stata analysis script, a Python analysis fallback, a Beamer deck, a Python-native Markdown fallback deck, and safe ignored output folders.

## Supporting Docs

- Stata/SPSS workflow: `docs/stata-extension.md`
- Beamer/Python slide workflow: `docs/latex-extension.md`
- Reproducibility notes: `docs/reproducibility.md`

These document the traditional economist stack and the fallback contract. The base repo should still produce slides even when Stata, LaTeX, Quarto, R, Node, Jinja2, and YAML are unavailable.

## Safety Defaults

- Raw exports stay under `data/<survey_key>/raw/` and are ignored by git.
- Processed data stays under `data/<survey_key>/processed/` and is ignored by git.
- Generated slide inputs and rendered decks are ignored by git.
- The generated `site/` directory is ignored by git and rebuilt by GitHub Actions from synthetic data.
- Live API actions require explicit commands and environment variables.
- API tokens are never printed intentionally by the scripts.
