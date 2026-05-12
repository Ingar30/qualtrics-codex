# Reproducibility Notes

The reproducible unit is one survey folder plus one slide folder:

```text
code/<survey_key>/survey_spec.json
code/<survey_key>/analysis/run.py
slides/<survey_key>/main.tex
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/
```

Stata-first workflows may also include:

```text
code/<survey_key>/cleaning/run.do
code/<survey_key>/figures/run.do
```

## Main Live Demo Contract

The main teaching loop is:

1. create the survey in Qualtrics from `survey_spec.json`;
2. generate synthetic rows for that survey;
3. submit those rows through Qualtrics;
4. export responses once;
5. analyze once;
6. build slides once.

Codex should verify credentials without printing them and ask before each live API action. Local CSVs under `build/fixtures/` are staging files for Qualtrics submission or offline checks; they are not the demo object of interest.

## Analysis Contract

`scripts/run_analysis.py` tries Stata first and falls back to Python. Stata workflows use SPSS/SAV exports and `import spss`. Python workflows use CSV exports and filter Qualtrics metadata rows when `ResponseId` exists.

All analysis paths should write:

```text
data/<survey_key>/processed/clean.csv
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/<figure>.pdf
slides/<survey_key>/inputs/<figure>.png
```

Use figure PDFs in Beamer. Use figure PNGs in the native HTML fallback.

## Slide Contract

`scripts/build_slides.py` tries Beamer first and falls back to native HTML slides. Beamer reads `slides/<survey_key>/main.tex` and generated PDF/table inputs. Native slides read `slides/<survey_key>/slides.md` and generated PNG/Markdown inputs.

Reusable Qualtrics links belong only in ignored `slides/<survey_key>/inputs/survey_link.tex` and `survey_link.md` files.

## Public Site Contract

The GitHub Pages site is built from generated synthetic discrimination-beliefs demo data only:

```bash
python scripts/build_site.py --output-dir site
```

The site may publish demo slides, demo tables, demo figures, and a walkthrough. It must not publish raw exports, processed real response data, survey IDs, reusable respondent links, Qualtrics metadata, local private paths, API tokens, or secret-loading files.
