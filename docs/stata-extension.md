# Stata Extension

The default starter workflow uses Python and CSV. Use this extension when you want Stata to import SPSS `.sav` exports and produce the analysis outputs.

## Recommended Additions

```text
code/<survey_key>/cleaning/run.do
code/<survey_key>/figures/run.do
scripts/run-stata-analysis.ps1
scripts/run-stata-do.ps1
```

Keep Stata files survey-specific and readable. Add comments before each major block so the workflow remains teachable.

## Environment

Set `STATA_EXE` to your Stata executable if it is not on PATH.

Windows PowerShell example:

```powershell
$env:STATA_EXE = "C:\Stata19\StataSE-64.exe"
```

macOS/Linux users should adapt the runner script to call their local Stata batch executable.

## Data Flow

1. Export SPSS from Qualtrics:

   ```bash
   python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
   ```

2. Stata imports the newest `.sav` under `data/<survey_key>/raw/`.
3. Stata writes `data/<survey_key>/processed/clean.dta`.
4. Stata writes slide inputs under `slides/<survey_key>/inputs/`.
5. Quarto can still render `slides/<survey_key>/slides.qmd` using Stata-generated figures.

## Codex Skill Tip

If you rely on Stata regularly, add a repo-local skill that tells Codex:

- where Stata lives on your machine;
- how to run batch `.do` files;
- where raw, processed, metadata, and slide-input files belong;
- that raw exports must not be edited after download.
