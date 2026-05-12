# Reproducibility Notes

The workflow has two public commands after a survey response export:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Before live Qualtrics responses exist, generate disposable local smoke-test responses only to check the analysis and slide path:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/build_slides.py --survey-key <survey_key>
```

This local smoke test does not call Qualtrics and should not write to `data/<survey_key>/raw/`. It is not the main live-demo output.

## Live Qualtrics Test Loop

The confirmed live path is:

```bash
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

The scripts hide survey IDs, response IDs, reusable links, tokens, and Qualtrics URLs from normal terminal output. `--write-slide-inputs` writes the reusable link only to ignored local slide input files.

## Conversational Loop

The repository is meant to support a single user request such as:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should interpret that as a live Qualtrics test loop. It should verify credentials without printing them and ask before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses. For a no-credentials smoke test, ask Codex to generate disposable local responses only to check analysis and slides.

## Analysis Contract

`scripts/run_analysis.py` tries Stata first and falls back to Python. It prefers the lab-style layout when present:

```text
code/<survey_key>/cleaning/run.do
code/<survey_key>/figures/run.do
scripts/stata/survey_pipeline.do
```

Otherwise it uses `code/<survey_key>/analysis/run.do`, then `code/<survey_key>/analysis/run.py`. All paths should write the same files:

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
