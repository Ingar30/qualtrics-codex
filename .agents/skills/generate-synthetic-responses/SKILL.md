---
name: generate-synthetic-responses
description: Use when the user asks Codex to generate synthetic survey responses locally or explicitly submit synthetic rows to Qualtrics for a live test survey.
metadata:
  short-description: Generate synthetic responses
---

# Generate Synthetic Responses

Default to local synthetic CSV generation before any live API submission.

## Local First

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
```

Survey specs may include `synthetic_weights` as either a list matching `choices` or an object keyed by choice label.

## Live Qualtrics Submission

Submit to Qualtrics only after explicit user approval. The safer live pattern is:

```bash
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --limit 1
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --resume
```

If the user explicitly wants one command, use `--smoke-then-rest`. Do not print response IDs; they are saved only in ignored local metadata.
