---
name: qualtrics-survey-loop
description: Use when the user asks Codex to create, test, download, analyze, or present a Qualtrics survey workflow with local synthetic responses, live Qualtrics draft/test links, Qualtrics exports, Stata/Python analysis, and Beamer/native slides.
metadata:
  short-description: Run Qualtrics survey workflow
---

# Qualtrics Survey Loop

Use this skill when the user asks Codex to create, test, download, analyze, or present a Qualtrics survey workflow.

The intended loop is:

1. The user asks for a survey from either detailed questions or a broad research/teaching idea.
2. Codex creates or updates `code/<survey_key>/survey_spec.json`, analysis scripts, and slide files.
3. Codex determines the next mode:
   - synthetic-only smoke test with no live API call;
   - live draft/test link, only after explicit user approval and local secrets are loaded;
   - export/download existing real responses, only after explicit user approval and local secrets are loaded.
4. Codex generates or downloads responses.
5. Codex cleans data with `scripts/run_analysis.py`, preferring Stata when available and falling back to Python.
6. Codex builds slides with `scripts/build_slides.py`, preferring Beamer when available and falling back to native HTML slides.
7. Codex reports artifact paths and the public/private boundary.

## Decision Rules

- If the user gives a broad survey idea, infer a simple 4-8 question survey and state the assumptions.
- Ask a short clarification only when the answer changes a live API action, privacy boundary, or core research design.
- Default to local synthetic responses before live Qualtrics calls.
- Treat "test link" as a live Qualtrics action: it requires local `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN`, and the user must explicitly ask for it.
- Treat "download responses" or "export responses" as a live Qualtrics read/export action: verify credentials are present without printing values.
- Treat API-created response submission as a live mutation even if the survey is draft or inactive.
- When cleaning Qualtrics CSV exports, filter metadata rows by keeping `ResponseId` values that start with `R_` when that column exists.
- Never print token values, survey metadata, reusable links, raw real response contents, or local secret file contents.

## Commands

Generate local synthetic responses:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
```

Analyze synthetic responses:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
```

Build slides:

```bash
python scripts/build_slides.py --survey-key <survey_key>
```

Create a live draft survey only after explicit approval:

```bash
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
```

Get a reusable anonymous link only after explicit approval:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key>
```

Export real responses only after explicit approval:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id SV_... --format csv
```

Analyze newest real local export:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

## Typical User Prompt

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures.
```

For that prompt, treat survey creation, synthetic response submission on Qualtrics, and export/download as live API actions. Verify credentials without printing them and ask before each live mutation/export. If the user wants a no-credentials smoke test, generate local synthetic responses instead.
