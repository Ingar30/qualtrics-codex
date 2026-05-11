---
name: create-qualtrics-survey
description: Use when the user asks Codex to create a live Qualtrics draft survey from code/<survey_key>/survey_spec.json using the repository helper, while keeping survey IDs and metadata private.
metadata:
  short-description: Create Qualtrics survey
---

# Create Qualtrics Survey

Use only after the user explicitly asks for a live Qualtrics survey action.

## Workflow

1. Verify `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` are set without printing values.
2. Confirm `code/<survey_key>/survey_spec.json` exists.
3. Run a lightweight auth check:

```bash
python scripts/qualtrics_workflow.py check-auth
```

4. Create the draft survey:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
```

Do not print or commit survey IDs, metadata, reusable links, or token values. Survey metadata is written under ignored `data/<survey_key>/metadata/`.
