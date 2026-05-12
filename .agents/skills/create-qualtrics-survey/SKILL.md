---
name: create-qualtrics-survey
description: Create a live Qualtrics draft survey from a simple JSON survey specification and save private local metadata for later link, export, or synthetic-response steps.
metadata:
  short-description: Create Qualtrics survey
---

# Create Qualtrics Survey

Use this only when the user explicitly asks for a live Qualtrics survey action.

## Workflow

Check credentials without printing values:

```bash
python scripts/qualtrics_workflow.py check-auth
```

Create a draft survey from a spec:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey name>" --spec-file code/<survey_key>/survey_spec.json
```

Activate only when the user explicitly intends to collect responses:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey name>" --spec-file code/<survey_key>/survey_spec.json --activate
```

## Expected Inputs

- `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` set in the shell.
- A simple JSON survey spec with short snake_case question tags.
- A folder-safe `survey_key`.

## Expected Outputs

- A live Qualtrics draft/test survey.
- Private ignored metadata under `data/<survey_key>/metadata/`.

## Safety

- Do not print or store API tokens.
- Do not print survey IDs unless a user explicitly needs them locally.
- Do not assume draft/inactive surveys are safe from API-created test responses.
- Use `get-link --write-slide-inputs` to save private slide-link inputs without printing the reusable link.
