# Reproducibility Notes

The workflow has two public commands after a survey response export:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Before real responses exist, generate disposable synthetic responses and run the same analysis path against them:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/build_slides.py --survey-key <survey_key>
```

This local smoke test does not call Qualtrics and should not write to `data/<survey_key>/raw/`.

## Analysis Contract

`scripts/run_analysis.py` tries Stata first and falls back to Python. Both paths should write the same files:

```text
data/<survey_key>/processed/clean.csv
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/<figure>.pdf
slides/<survey_key>/inputs/<figure>.png
```

Use figure PDFs in Beamer. Use figure PNGs in the Python HTML fallback.

## Slide Contract

`scripts/build_slides.py` tries Beamer first and falls back to Python. Beamer reads:

```text
slides/<survey_key>/main.tex
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/*.pdf
```

The Python fallback reads:

```text
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/*.png
```

## Force A Backend

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
python scripts/run_analysis.py --survey-key <survey_key> --mode python
python scripts/build_slides.py --survey-key <survey_key> --mode beamer
python scripts/build_slides.py --survey-key <survey_key> --mode python
```

Forced modes are useful for debugging. The default `auto` mode is for collaborators who may not have the same local tools installed.

## Public Site Contract

The GitHub Pages site is built from generated synthetic data only:

```bash
python scripts/build_site.py --output-dir site
```

The site may publish demo slides, demo tables, demo figures, and a walkthrough. It must not publish:

- raw Qualtrics exports;
- processed real response data;
- survey IDs or reusable respondent links;
- Qualtrics metadata;
- local paths containing private project details;
- API tokens or secret-loading files.

Live Qualtrics validation is a local/manual loop unless a user explicitly opts into a separate secret-backed workflow.
