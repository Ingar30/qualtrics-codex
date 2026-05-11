# AGENTS.md

Instructions for Codex and other automation agents working in this starter repo.

## Goals

- Keep the default workflow easy to adopt: Stata/Beamer first when available, Python/native HTML fallback when not.
- Keep live Qualtrics work local by default. The public Pages site uses synthetic fixture data only.
- Prefer small, readable changes over framework-heavy abstractions.

## Safety

- Never print, log, or commit values from variables containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, or `AUTH`.
- Never commit `.env`.
- Prefer local secrets under `$HOME\.secrets\qualtrics.env.ps1`; never write that file into the repository.
- Do not edit files under `data/<survey_key>/raw/` after export unless explicitly asked.
- Do not create, activate, delete, or modify live Qualtrics surveys unless the user explicitly requests that API action.
- Prefer draft survey creation. Use activation flags only when the user intends to collect responses.
- Do not publish raw exports, processed real data, survey IDs, reusable links, or Qualtrics metadata to GitHub Pages by default.

## Layout

```text
code/<survey_key>/survey_spec.json
code/<survey_key>/analysis/run.do
code/<survey_key>/analysis/run.py
data/<survey_key>/raw/
data/<survey_key>/processed/
data/<survey_key>/metadata/
slides/<survey_key>/main.tex
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/
scripts/
docs/
prompts/
site/
```

## Defaults

- Python handles Qualtrics API calls, CSV import, cleaning, tables, and figures.
- `scripts/run_analysis.py` tries Stata first and falls back to Python.
- `scripts/build_slides.py` tries Beamer first and falls back to native HTML slides.
- `scripts/render_slides.py` handles Markdown-to-HTML slide rendering with the Python standard library.
- `scripts/build_site.py` builds the synthetic-data public Pages site.
