# Live Validation

The README is the public entry point. This file documents the guarded validation sequence behind that workflow.

Public validation stays offline. CI and GitHub Pages never call Qualtrics, never submit responses, and never publish live survey links.

## What Was Validated Locally

A local live run validated the main teaching loop:

- create a Qualtrics test survey from a JSON spec;
- save the reusable anonymous link only in private local metadata and ignored slide inputs;
- prepare 100 synthetic response rows and submit them through Qualtrics;
- export responses once;
- clean to 100 rows, generate figures, and build slides.

Only this sanitized validation shape belongs in the public repository. Do not publish survey IDs, response IDs, reusable links, raw rows, live export paths, or metadata contents.

For analysis preferences, use SPSS/SAV exports for Stata workflows and CSV exports for Python workflows.

## Lean Helper

Use the helper when you explicitly want a local run that calls Qualtrics:

```powershell
python scripts/run_live_validation.py `
  --survey-key "<survey_key>" `
  --survey-name "<survey name>" `
  --spec-file "code/<survey_key>/survey_spec.json" `
  --n 100
```

Inspect the command sequence without calling Qualtrics:

```powershell
python scripts/run_live_validation.py `
  --survey-key "<survey_key>" `
  --survey-name "<survey name>" `
  --spec-file "code/<survey_key>/survey_spec.json" `
  --n 100 `
  --dry-run
```

The helper streams command output to the local terminal so students can see progress. It does not store survey IDs, response IDs, reusable links, raw rows, tokens, Qualtrics URLs, or metadata contents in its summary. The sanitized summary is written under `data/<survey_key>/metadata/`, which is ignored by git.

Use `--export-format spss` when validating the Stata/SAV path. Use the default `--export-format csv` for Python-first validation.

## Cleanup

Live validation creates a draft or test survey in Qualtrics. After validation, open Qualtrics and manually archive or delete the test survey if you no longer need it.

This iteration intentionally does not add an API delete command for surveys. Keep cleanup visible and manual.
