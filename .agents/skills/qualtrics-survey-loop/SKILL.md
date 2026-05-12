---
name: qualtrics-survey-loop
description: Use when the user asks Codex to run the main live Qualtrics teaching loop: create a survey, submit synthetic responses through Qualtrics, export, analyze, and build slides.
metadata:
  short-description: Run Qualtrics teaching loop
---

# Qualtrics Survey Loop

Use this skill for the main live teaching demo.

The intended loop is:

1. Offer `prompts/configure-local-preferences.md` on first use or when local preferences are unclear.
2. Create or update `code/<survey_key>/survey_spec.json`, analysis scripts, and slide files.
3. Verify Qualtrics credentials are present without printing values.
4. Ask before each live API action: create survey, get link, submit synthetic responses, or export responses.
5. Generate synthetic rows as a staging file, submit them through Qualtrics, export once, analyze once, and build slides.
6. Report artifact paths and the public/private boundary.

## Decision Rules

- If the user gives a broad survey idea, infer a simple 4-8 question survey and state the assumptions.
- Ask a short clarification only when the answer changes live API use, privacy, or core survey design.
- Bias toward creating the survey in Qualtrics and submitting Codex-generated synthetic responses there for the teaching demo.
- Use local synthetic rows only as staging files or for an explicitly requested offline check.
- If the user chooses Stata, export/download Qualtrics responses as SPSS/SAV and import with Stata. If the user chooses Python, export/download responses as CSV and analyze with Python.
- Use `check-auth` for the first read-only API check.
- Treat API-created response submission as a live mutation even if the survey is draft or inactive.
- Save reusable links to ignored slide inputs with `get-link --write-slide-inputs` instead of printing them.
- Preserve `slides/<survey_key>/inputs/survey_link.tex` and `survey_link.md` when analysis regenerates slide inputs.
- Never print token values, survey metadata, reusable links, survey IDs, response IDs, raw response contents, or local secret file contents.

## Main Command Shape

```bash
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Use `--format spss` for the Stata/SAV path.

## Typical User Prompt

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```
