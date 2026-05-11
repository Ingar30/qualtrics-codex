# AGENTS.md

Instructions for Codex and other automation agents working in this starter repo.

## Goals

- Keep the default workflow easy to adopt: Python, CSV, and native HTML slides.
- Keep optional Stata and LaTeX paths isolated in extension docs.
- Prefer small, readable changes over framework-heavy abstractions.

## Safety

- Never print, log, or commit values from variables containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, or `AUTH`.
- Never commit `.env`.
- Do not edit files under `data/<survey_key>/raw/` after export unless explicitly asked.
- Do not create, activate, delete, or modify live Qualtrics surveys unless the user explicitly requests that API action.
- Prefer draft survey creation. Use activation flags only when the user intends to collect responses.

## Layout

```text
code/<survey_key>/survey_spec.json
code/<survey_key>/analysis/run.py
data/<survey_key>/raw/
data/<survey_key>/processed/
data/<survey_key>/metadata/
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/
scripts/
docs/
prompts/
```

## Defaults

- Python handles Qualtrics API calls, CSV import, cleaning, tables, and figures.
- `scripts/render_slides.py` handles Markdown-to-HTML slide rendering with the Python standard library.
- Stata and LaTeX are optional extensions; if used, document required executable locations and add focused instructions or skills.
