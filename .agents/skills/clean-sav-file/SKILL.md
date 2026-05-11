---
name: clean-sav-file
description: Use when the user asks Codex to clean a Qualtrics SPSS .sav export with Stata using lab-style code/<survey_key>/cleaning/run.do and scripts/stata/survey_pipeline.do.
metadata:
  short-description: Clean SAV with Stata
---

# Clean SAV File

Use this for the Stata/SPSS path:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

If present, `scripts/run_analysis.py` prefers:

```text
code/<survey_key>/cleaning/run.do
code/<survey_key>/figures/run.do
scripts/stata/survey_pipeline.do
```

The wrapper can analyze `.sav` exports with Stata and falls back to Python only for CSV-compatible workflows. Keep `data/<survey_key>/raw/` immutable after export.
