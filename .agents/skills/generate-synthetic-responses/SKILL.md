---
name: generate-synthetic-responses
description: Generate local synthetic response CSVs, or submit synthetic rows to Qualtrics only when the user explicitly asks for live API-created test responses.
metadata:
  short-description: Generate synthetic responses
---

# Generate Synthetic Responses

Default to local synthetic CSV generation. Treat submission to Qualtrics as a live mutation.

## Local Synthetic Rows

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --spec-file code/<survey_key>/survey_spec.json --output build/fixtures/<survey_key>_responses.csv --n 100
```

Use these rows for a no-credentials smoke test:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/build_slides.py --survey-key <survey_key>
```

## Live Synthetic Submission

Only after explicit authorization and loaded Qualtrics credentials:

```bash
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --limit 1
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --resume
```

For a Stata validation path, export with `--format spss` after submission. For a Python validation path, export with `--format csv`.

## Safety

- Prefer local synthetic responses before live API calls.
- Submit one row first, export/analyze/build, then resume remaining rows.
- Do not use production surveys for synthetic API-created responses.
- Never print tokens, response IDs, raw rows, or reusable links.
