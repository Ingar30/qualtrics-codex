---
name: clean-sav-file
description: Use Stata to import a Qualtrics SPSS .sav export with import spss, clean it to clean.dta, and prepare slide inputs for Stata-first workflows.
metadata:
  short-description: Clean SAV with Stata
---

# Clean SAV File

Use this only for the Stata/SPSS path. If the user chooses Python, export CSV instead and use Python analysis.

## Workflow

Download or use an existing SPSS/SAV export:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
```

Run the Stata path:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

Windows compatibility wrapper:

```powershell
.\scripts\run-stata-analysis.ps1 -SurveyKey "<survey_key>"
```

## Expected Stata Behavior

- Import the newest `.sav` with `import spss`.
- Apply survey-specific cleaning in `code/<survey_key>/cleaning/run.do` when present.
- Save `data/<survey_key>/processed/clean.dta`.
- Write slide inputs such as `summary.tex`, `cleaning_report.tex`, and figure PDFs under `slides/<survey_key>/inputs/`.
- Move Stata logs to ignored `data/<survey_key>/metadata/`.

## Safety

- Treat `data/<survey_key>/raw/` as immutable after export.
- Do not publish `.sav`, `.dta`, export metadata, survey IDs, response IDs, or reusable links.
- Stop on Stata errors and inspect the log before rebuilding slides.
