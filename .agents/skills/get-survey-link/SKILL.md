---
name: get-survey-link
description: Retrieve or construct the reusable anonymous Qualtrics link for an existing survey and save it to ignored local metadata and slide inputs.
metadata:
  short-description: Get survey link
---

# Get Survey Link

Use this when the user needs a local reusable Qualtrics test/respondent link.

## Command

Save link inputs without printing the link:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
```

Use a respondent-facing branded host when the API datacenter host is not the public survey host:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --public-host <brand>.qualtrics.com --write-slide-inputs
```

Print the link only when the user explicitly needs to see it locally:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --show-private-link
```

## Expected Outputs

- Ignored local metadata under `data/<survey_key>/metadata/`.
- Ignored slide inputs:
  - `slides/<survey_key>/inputs/survey_link.tex`
  - `slides/<survey_key>/inputs/survey_link.md`

## Safety

- Do not publish reusable links to GitHub Pages.
- Do not print links by default.
- Preserve private link inputs through analysis/build steps.
- State in slide inputs that the survey must be activated before the respondent-facing link can be used.
- If the link says inactive, inspect survey status and flow in Qualtrics rather than modifying the survey without user approval.
