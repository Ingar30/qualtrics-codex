---
name: qualtrics-survey-loop
description: Use when the user asks Codex to create, test, download, analyze, or present a Qualtrics survey workflow with a live Qualtrics test survey, synthetic responses submitted to Qualtrics, Qualtrics exports, Stata/Python analysis, and Beamer/native slides.
metadata:
  short-description: Run Qualtrics survey workflow
---

# Qualtrics Survey Loop

Use this skill when the user asks Codex to create, test, download, analyze, or present a Qualtrics survey workflow.

The intended loop is:

1. The user asks for a survey from either detailed questions or a broad research/teaching idea.
2. Codex offers `prompts/configure-local-preferences.md` on first use or when local preferences are unclear, then uses ignored `AGENTS.override.md` if present.
3. Codex creates or updates `code/<survey_key>/survey_spec.json`, analysis scripts, and slide files.
4. Codex determines the next mode:
   - local smoke test with no live API call, only to check analysis and slides;
   - live draft/test link and synthetic response submission, only after explicit user approval and local secrets are loaded;
   - export/download existing real responses, only after explicit user approval and local secrets are loaded.
5. Codex prepares synthetic rows for smoke tests or Qualtrics submission, submits them to Qualtrics for the live demo, or downloads real responses.
6. Codex cleans data with `scripts/run_analysis.py`, using SPSS/SAV exports for Stata workflows and CSV exports for Python workflows.
7. Codex builds slides with `scripts/build_slides.py`, preferring Beamer when available and falling back to native HTML slides.
8. Codex reports artifact paths and the public/private boundary.

## Decision Rules

- If the user gives a broad survey idea, infer a simple 4-8 question survey and state the assumptions.
- Ask a short clarification only when the answer changes a live API action, privacy boundary, or core research design.
- Use local synthetic responses only for smoke tests or as staging files for Qualtrics submission. For a live teaching demo, bias toward creating the survey in Qualtrics and submitting synthetic responses there. Use `scripts/run_live_validation.py --dry-run` when packaging or explaining the lean live demo loop.
- If the user chooses Stata, export/download Qualtrics responses as SPSS/SAV and import with Stata. If the user chooses Python, export/download responses as CSV and analyze with Python.
- For live credentials, use `check-auth` rather than `list-surveys`; full listing is only for explicit survey browsing.
- Treat "test link" as a live Qualtrics action: it requires local `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN`, and the user must explicitly ask for it.
- Treat "download responses" or "export responses" as a live Qualtrics read/export action: verify credentials are present without printing values.
- Treat API-created response submission as a live mutation even if the survey is draft or inactive.
- Submit generated synthetic rows in one step for the default teaching demo, then export once, analyze once, and build slides.
- When the user asks to include the reusable link in slides, save it to ignored slide inputs with `get-link --write-slide-inputs` instead of printing it.
- Preserve `slides/<survey_key>/inputs/survey_link.tex` and `survey_link.md` when analysis regenerates slide inputs.
- When cleaning Qualtrics CSV exports, filter metadata rows by keeping `ResponseId` values that start with `R_` when that column exists.
- Never print token values, survey metadata, reusable links, survey IDs, response IDs, raw real response contents, or local secret file contents.
- Use the granular skills in this repo when a user asks for one part of the loop: `create-qualtrics-survey`, `generate-synthetic-responses`, `download-qualtrics-sav`, `clean-sav-file`, `stata-figures`, `beamer-slides`, `get-survey-link`, and `slide-review-panel`.

## Commands

Prepare local smoke-test or submission rows:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
```

Analyze local smoke-test rows:

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
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Get a reusable anonymous link only after explicit approval:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
```

Export real responses only after explicit approval:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id <survey_id> --format csv
```

Download SPSS/SAV for the lab-style Stata path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

Export CSV for the Python path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key> --mode python
```

Run the lean live validation helper only after explicit approval:

```bash
python scripts/run_live_validation.py --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json --n 100
```

Analyze newest real local export:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

## Typical User Prompt

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

For that prompt, treat survey creation, synthetic response submission on Qualtrics, and export/download as live API actions. Verify credentials without printing them and ask before each live mutation/export. If the user wants a no-credentials smoke test, generate disposable local responses only to check analysis and slides.
