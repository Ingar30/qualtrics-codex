---
name: download-qualtrics-sav
description: Download Qualtrics responses as an SPSS/SAV export for Stata workflows.
metadata:
  short-description: Download Qualtrics SAV
---

# Download Qualtrics SAV

Use this when the user chooses Stata or explicitly asks for a Qualtrics SPSS/SAV export. If the user chooses Python, use CSV export instead.

## Command

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
```

Compatibility alias:

```bash
python scripts/qualtrics_workflow.py export-spss --survey-key <survey_key>
```

Prefer saved local metadata or an explicit `--survey-id` when exporting. Use survey-name lookup only when needed.

## Expected Outputs

- A timestamped ignored raw export folder under `data/<survey_key>/raw/`.
- The downloaded Qualtrics export ZIP.
- The extracted `.sav` file.
- Ignored export metadata under `data/<survey_key>/metadata/` or the raw timestamp folder.

## Safety

- Export live responses only after explicit user authorization.
- Never print tokens, survey IDs, response IDs, reusable links, raw rows, or metadata contents.
- Keep raw exports immutable and out of git.
- After export, run Stata import/cleaning with `python scripts/run_analysis.py --survey-key <survey_key> --mode stata`.
