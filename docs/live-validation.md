# Live Validation

This repository keeps public validation offline by default. CI and GitHub Pages never call Qualtrics, never submit responses, and never publish live survey links.

## What Was Validated Locally

A local live run validated the repository command loop directly:

- A Qualtrics test survey was created from a JSON spec.
- The reusable anonymous link was saved only in private local metadata and ignored slide inputs.
- 100 synthetic responses were generated locally and submitted to Qualtrics.
- Responses were exported, cleaned to 100 rows, and charted.
- Beamer output and native HTML/PDF slide output were built from generated inputs.

That test validated the repository commands and scripts. It did not validate a second autonomous Codex process operating with live credentials.

On May 12, 2026, the same command loop was also exercised with this public-opinion prompt:

```text
Create a public opinion survey on labor market concerns and support for immigration in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

The local run completed with 100 synthetic Qualtrics submissions, a response export cleaned to 100 rows, generated figures, a Beamer PDF, native slide output, and private survey-link slide inputs. The public repository should record only this sanitized result; do not publish survey IDs, response IDs, reusable links, raw rows, live export paths, or metadata contents.

For analysis preferences, use SPSS/SAV exports for Stata workflows and CSV exports for Python workflows. This keeps the Stata path close to the standard Qualtrics-to-Stata teaching workflow while keeping the Python path simple and cross-platform.

## Guarded Helper

Use the helper when you explicitly want a local run that calls Qualtrics:

```powershell
python scripts/run_live_validation.py `
  --survey-key "<survey_key>" `
  --survey-name "<survey name>" `
  --spec-file "code/<survey_key>/survey_spec.json" `
  --n 100 `
  --i-understand-this-calls-qualtrics
```

Inspect the command sequence without calling Qualtrics:

```powershell
python scripts/run_live_validation.py `
  --survey-key "<survey_key>" `
  --survey-name "<survey name>" `
  --spec-file "code/<survey_key>/survey_spec.json" `
  --n 100 `
  --dry-run `
  --i-understand-this-calls-qualtrics
```

The helper captures command output and does not print survey IDs, response IDs, reusable links, raw rows, tokens, Qualtrics URLs, or metadata contents. It writes only a sanitized summary under `data/<survey_key>/metadata/`, which is ignored by git.

Use `--export-format spss` when validating the Stata/SAV path. Use the default `--export-format csv` for Python-first validation.

## Cleanup

Live validation creates a draft or test survey in Qualtrics. After validation, open Qualtrics and manually archive or delete the test survey if you no longer need it.

This iteration intentionally does not add an API delete command for surveys. Keep cleanup visible and manual.
