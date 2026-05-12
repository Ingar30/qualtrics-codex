---
name: generate-synthetic-responses
description: Prepare synthetic rows for the main Qualtrics workflow and submit them to a live Qualtrics test survey after explicit approval.
metadata:
  short-description: Generate synthetic responses
---

# Generate Synthetic Responses

Local CSVs are supporting files. For the normal live Qualtrics workflow, create the survey in Qualtrics, prepare synthetic rows, submit them to that Qualtrics test survey, export the responses, then analyze and build slides. Treat submission to Qualtrics as a live mutation.

## Prepare Staging Rows

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --spec-file code/<survey_key>/survey_spec.json --output build/fixtures/<survey_key>_responses.csv --n 100
```

Use these rows for Qualtrics submission. Use them for offline analysis checks only when the user explicitly asks to avoid live Qualtrics calls:

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

- Local synthetic CSVs are not the object of interest; they are staging files for Qualtrics submission or explicit offline checks.
- Submit generated rows in one step for the default workflow.
- Do not use production surveys for synthetic API-created responses.
- Never print tokens, response IDs, raw rows, or reusable links.
