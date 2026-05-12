---
name: generate-synthetic-responses
description: Prepare disposable local smoke-test rows, or submit synthetic rows to a live Qualtrics test survey when the user asks for the full Qualtrics demo loop.
metadata:
  short-description: Generate synthetic responses
---

# Generate Synthetic Responses

Local CSVs are supporting files. For the normal live teaching demo, create the survey in Qualtrics, prepare synthetic rows, submit them to that Qualtrics test survey, export the responses, then analyze and build slides. Treat submission to Qualtrics as a live mutation.

## Local Smoke-Test Rows

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --spec-file code/<survey_key>/survey_spec.json --output build/fixtures/<survey_key>_responses.csv --n 100
```

Use these rows only for a no-credentials smoke test of analysis and slides:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/build_slides.py --survey-key <survey_key>
```

## Qualtrics Synthetic Submission

Only after explicit authorization and loaded Qualtrics credentials, submit the prepared rows to the live test survey:

```bash
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
```

For a Stata validation path, export with `--format spss` after submission. For a Python validation path, export with `--format csv`.

## Safety

- Use local synthetic rows only when checking that analysis and slides work without credentials.
- Local synthetic CSVs are not the object of interest; they are either smoke-test fixtures or staging files for Qualtrics submission.
- Submit generated rows in one step for the default teaching demo.
- Do not use production surveys for synthetic API-created responses.
- Never print tokens, response IDs, raw rows, or reusable links.
