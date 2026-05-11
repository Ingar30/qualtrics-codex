# Qualtrics Research Workflow Starter

A small starter repository for researchers who want a reproducible path from a Qualtrics survey to cleaned data, figures, and HTML slides.

The default workflow is deliberately low-friction:

1. Write a simple JSON survey specification.
2. Use Python to create or connect to a Qualtrics survey.
3. Export responses as CSV.
4. Analyze the CSV with Python.
5. Render browser-based slides with the built-in Python slide renderer.

Stata and LaTeX/Beamer are supported as optional extensions, not required for the first run.

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
python code/repo_smoke_test/analysis/run.py --input tests/fixtures/repo_smoke_test_responses.csv
python scripts/render_slides.py --survey-key repo_smoke_test
```

The rendered slide deck is written to:

```text
build/slides/repo_smoke_test/slides.html
```

## Configure Qualtrics

Copy the example environment file and fill in your local values:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Required variables:

```text
QUALTRICS_API_TOKEN=...
QUALTRICS_DATACENTER=...
```

Optional:

```text
QUALTRICS_PUBLIC_HOST=yourbrand.qualtrics.com
```

Never commit `.env` or API tokens.

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
python code/repo_smoke_test/analysis/run.py
python scripts/render_slides.py --survey-key repo_smoke_test
```

## Scaffold A New Project With Codex

Use the prompt in:

```text
prompts/scaffold-workflow.md
```

It asks Codex to create a new `code/<survey_key>/` folder, a Python analysis script, a Markdown slide deck, and safe ignored output folders.

## Optional Extensions

- Stata/SPSS workflow: `docs/stata-extension.md`
- LaTeX/Beamer or PDF workflow: `docs/latex-extension.md`

These are useful if you want the more traditional economist stack. The base repo should still run without Stata, LaTeX, Quarto, R, or Node.

## Safety Defaults

- Raw exports stay under `data/<survey_key>/raw/` and are ignored by git.
- Processed data stays under `data/<survey_key>/processed/` and is ignored by git.
- Generated slide inputs and rendered decks are ignored by git.
- Live API actions require explicit commands and environment variables.
- API tokens are never printed intentionally by the scripts.
