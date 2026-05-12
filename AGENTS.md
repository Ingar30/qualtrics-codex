# AGENTS.md

Instructions for Codex and other automation agents working in this starter repo.

## Goals

- Keep the default workflow easy to adopt: Stata/Beamer first when available, Python/native HTML fallback when not.
- Keep live Qualtrics work local by default. The public Pages site uses synthetic fixture data only.
- Prefer small, readable changes over framework-heavy abstractions.
- Support the intended user loop: a researcher asks Codex for a survey from either detailed instructions or a broad idea; Codex scaffolds the survey, asks or infers whether the user wants synthetic responses, a live draft/test link, or an export of existing responses, then cleans data and builds figures/slides.

## Safety

- Never print, log, or commit values from variables containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, or `AUTH`.
- Never commit `.env`.
- Prefer local secrets under `$HOME\.secrets\qualtrics.env.ps1`; never write that file into the repository.
- Do not edit files under `data/<survey_key>/raw/` after export unless explicitly asked.
- Do not create, activate, delete, or modify live Qualtrics surveys unless the user explicitly requests that API action.
- Prefer draft survey creation. Use activation flags only when the user intends to collect responses.
- Do not assume draft/inactive Qualtrics surveys cannot receive API-created test responses; treat API response submission as a live mutation.
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

- Python handles Qualtrics API calls, local synthetic CSV generation, and fallback cleaning/tables/figures.
- `scripts/run_analysis.py` tries lab-style Stata cleaning/figures first when present, then compact Stata analysis, then Python.
- `scripts/build_slides.py` tries Beamer first and falls back to native HTML slides.
- `scripts/render_slides.py` handles Markdown-to-HTML slide rendering with the Python standard library.
- `scripts/build_site.py` builds the synthetic-data public Pages site.
- Qualtrics CSV exports often include metadata rows after the header; cleaning code should keep real rows where `ResponseId` starts with `R_` when that column exists.
- Stata workflows should use Qualtrics SPSS/SAV export (`export-responses --format spss`) and Stata `import spss`.
- Python workflows should use Qualtrics CSV export (`export-responses --format csv`) and Python analysis.

## Local Preferences

On first use, or when workflow preferences are unclear, offer the user `prompts/configure-local-preferences.md`.
Before asking those preference questions, inspect local tool availability for Python dependencies, Stata, LaTeX/Beamer, and Qualtrics environment variables.
Report only presence or absence for secrets; never print values and never ask users to paste API tokens into Codex.
If the user answers, summarize their choices in ignored `AGENTS.override.md`; never store secrets there.
If the user does not answer, continue with the default setup: Stata-first when available, Python fallback, Beamer-first with native fallback, CSV for Python, SAV for Stata, local synthetic smoke tests before live Qualtrics calls, and public Pages synthetic-only.

## Expected Agent Loop

When the user asks for a survey workflow, use the repo-local skill in `.agents/skills/qualtrics-survey-loop/` if available.

Default to a synthetic local smoke test first. Before live Qualtrics actions, distinguish among:

- draft/test link: create or use a live draft survey and retrieve the reusable link;
- synthetic responses: generate local fake responses for testing, or submit fake responses only if the user explicitly asks for live API submission;
- live synthetic test: submit one row first, export/check locally, then use `--resume` or `--smoke-then-rest` only after explicit approval;
- real responses: export/download from Qualtrics, keep raw files ignored, clean with Stata or Python, then build figures and slides.

Ad hoc `code/<survey_key>/` and `slides/<survey_key>/` folders are ignored by default. Promote only public-safe demos by editing `.gitignore` intentionally.
