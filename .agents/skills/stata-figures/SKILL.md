---
name: stata-figures
description: Generate Stata figure PDFs from a cleaned survey dataset and save them as slide inputs for Beamer/native decks.
metadata:
  short-description: Generate Stata figures
---

# Stata Figures

Use this for Stata-first workflows after a SAV export has been imported and cleaned.

## Workflow

Run the Stata analysis path:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

Windows compatibility wrapper:

```powershell
.\scripts\run-stata-analysis.ps1 -SurveyKey "<survey_key>"
```

## Expected Inputs

- A SAV export under `data/<survey_key>/raw/`.
- `code/<survey_key>/cleaning/run.do` and `code/<survey_key>/figures/run.do` for lab-style workflows, or `code/<survey_key>/analysis/run.do` for compact Stata workflows.
- Stata discoverable on PATH or through `STATA_EXE`.

## Expected Outputs

- `data/<survey_key>/processed/clean.dta`.
- Summary tables under `slides/<survey_key>/inputs/`.
- Figure PDFs for Beamer and PNGs when the workflow also supports native slides.
- Stata logs under ignored `data/<survey_key>/metadata/`.

## Safety

- Generate outputs from cleaned data; do not edit raw exports.
- Keep chart choices simple and readable.
- Skip missing variables with a clear report rather than silently fabricating figures.
- Rebuild slides after figures change.
