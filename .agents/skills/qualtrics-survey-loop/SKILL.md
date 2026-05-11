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
5. Codex cleans data with `scripts/run_analysis.py`, preferring lab-style Stata cleaning/figures when available and falling back to Python for CSV workflows.
6. Codex builds slides with `scripts/build_slides.py`, preferring Beamer when available and falling back to native HTML slides.
7. Codex reports artifact paths and the public/private boundary.

## Decision Rules

- If the user gives a broad survey idea, infer a simple 4-8 question survey and state the assumptions.
- Ask a short clarification only when the answer changes a live API action, privacy boundary, or core research design.
- Default to local synthetic responses before live Qualtrics calls.
- For live credentials, use `check-auth` rather than `list-surveys`; full listing is only for explicit survey browsing.
- Treat "test link" as a live Qualtrics action: it requires local `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN`, and the user must explicitly ask for it.
- Treat "download responses" or "export responses" as a live Qualtrics read/export action: verify credentials are present without printing values.
- Treat API-created response submission as a live mutation even if the survey is draft or inactive.
- Submit one synthetic response first when validating a new live survey, export/check locally, then continue with `--resume` or use `--smoke-then-rest` only when the user explicitly wants the one-command path.
- When cleaning Qualtrics CSV exports, filter metadata rows by keeping `ResponseId` values that start with `R_` when that column exists.
- Never print token values, survey metadata, reusable links, survey IDs, response IDs, raw real response contents, or local secret file contents.
- Use the granular skills in this repo when a user asks for one part of the loop: `create-qualtrics-survey`, `generate-synthetic-responses`, `download-qualtrics-sav`, `clean-sav-file`, `stata-figures`, `beamer-slides`, `get-survey-link`, and `slide-review-panel`.

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
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
```

Submit synthetic responses to Qualtrics only after explicit approval:

```bash
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --limit 1
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --resume
```

Get a reusable anonymous link only after explicit approval:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key>
```

Export real responses only after explicit approval:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id SV_... --format csv
```

Download SPSS/SAV for the lab-style Stata path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
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
