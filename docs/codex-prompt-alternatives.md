# Codex Prompt Alternatives

You can run the commands yourself, or you can ask Codex to run them after it has inspected the repository. These prompts are intentionally plain so new users do not need to know the scripts yet.

Do not paste Qualtrics API tokens into Codex. Store them locally first, then ask Codex to verify that the expected environment variables are present without printing values.

## Clone And Open

Command:

```bash
git clone https://github.com/Ingar30/qualtrics-codex.git
cd qualtrics-codex
codex
```

Prompt alternative:

```text
Clone https://github.com/Ingar30/qualtrics-codex into this folder, inspect the README, and validate the synthetic demo workflow without calling Qualtrics.
```

## Local Preferences First

Reusable prompt:

```text
Open prompts/configure-local-preferences.md and follow it as instructions for this Codex session. Do not summarize it. Inspect Python, Stata, LaTeX, and Qualtrics environment-variable status first. If Stata, LaTeX, or Qualtrics secrets are missing, tell me where to configure them or which fallback to use. Then ask the needed follow-up questions and save my answers in ignored AGENTS.override.md without secrets.
```

Plain-language version:

```text
Ask me about my local preferences for this Qualtrics workflow before we build anything. First inspect Python, Stata, LaTeX, and Qualtrics environment-variable status without printing secrets. If Stata, LaTeX, or Qualtrics secrets are missing, tell me where to configure them or which fallback to use. Then ask the needed follow-up questions and save my answers in ignored AGENTS.override.md without secrets.
```

## Scaffold A New Workflow

Prompt:

```text
Create a new Qualtrics research workflow using prompts/start-with-codex.md. Use survey_key <survey_key>, survey_name <survey_name>, topic <topic>, and audience <audience>. Use disposable local responses only if they help smoke-test analysis and slides. Do not call the live Qualtrics API.
```

## Full Survey-To-Slides Loop

Canonical prompt:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

This is a live API workflow. Codex should verify credentials without printing them and ask before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses. If slides should include the link, Codex should save it with `get-link --write-slide-inputs` rather than printing it.
For Stata workflows, export SPSS/SAV. For Python workflows, export CSV.

Prompt for the lean live test:

```text
Create the Qualtrics draft survey, prepare 100 synthetic rows for that survey, submit them to the Qualtrics test survey, export the responses once, clean them, and build slides. Keep credentials, metadata, response IDs, and reusable links private.
```

Local-only prompt:

```text
Create a public opinion survey on beliefs about discrimination in hiring. Use survey_key discrimination_beliefs. Generate 100 disposable local smoke-test responses, clean the generated data with Stata if available and Python otherwise, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Do not call the live Qualtrics API.
```

Prompt for a live test link:

```text
Create the live Qualtrics survey as a draft and save the reusable test link to ignored slide inputs. Verify QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values. Do not activate the survey unless I ask.
```

Prompt for real responses after data collection:

```text
Export the real Qualtrics responses for discrimination_beliefs, clean the newest local export in Stata if available and Python otherwise, regenerate figures, and rebuild the slides. Keep raw data, processed real data, metadata, and reusable links private by default.
```

Stata-specific real-response prompt:

```text
Export the real Qualtrics responses for <survey_key> as SPSS/SAV, import the .sav file with Stata, clean it to clean.dta, regenerate Stata figures, and rebuild the Beamer/native slides. Keep raw exports, metadata, and reusable links private.
```

Python-specific real-response prompt:

```text
Export the real Qualtrics responses for <survey_key> as CSV, clean the newest CSV export with Python, regenerate figures, and rebuild the slides. Filter Qualtrics metadata rows by keeping ResponseId values that start with R_ when that column exists.
```

## Fresh Synthetic Demo

Command:

```bash
python scripts/generate_synthetic_responses.py --survey-key repo_smoke_test --output build/fixtures/repo_smoke_test_responses.csv
python scripts/run_analysis.py --survey-key repo_smoke_test --input build/fixtures/repo_smoke_test_responses.csv
python scripts/build_slides.py --survey-key repo_smoke_test
```

Prompt alternative:

```text
Run the repository smoke test without calling Qualtrics: generate disposable local responses for repo_smoke_test, analyze them, and build the slides. If Stata or LaTeX is missing, use the repository fallbacks.
```

## Install Requirements

Command:

```powershell
.\scripts\setup.ps1
```

Prompt alternative:

```text
Set up the Python environment for this repository. Prefer a local .venv, install requirements.txt, and if venv creation fails, explain the safe fallback using scripts/setup.ps1 -User.
```

## Build The Public Demo Site

Command:

```bash
python scripts/build_site.py --output-dir site
```

Prompt alternative:

```text
Build the GitHub Pages demo site from synthetic data only. Do not call Qualtrics and do not use secrets.
```

## Set Up Local Qualtrics Secrets

Command:

```powershell
New-Item -ItemType Directory -Force $HOME\.secrets
notepad $HOME\.secrets\qualtrics.env.ps1
```

Prompt alternative:

```text
Show me where to store my Qualtrics API token and datacenter outside this repository. Give Windows and macOS/Linux examples. Do not ask me to paste token values into Codex.
```

## Check That Secrets Are Loaded

Command:

```powershell
if ($env:QUALTRICS_DATACENTER -and $env:QUALTRICS_API_TOKEN) { "Qualtrics env vars are set" }
```

Prompt alternative:

```text
Check whether QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set in my shell without printing their values.
```

## List Surveys

Command:

```bash
python scripts/qualtrics_workflow.py check-auth
```

Prompt alternative:

```text
Use the local Qualtrics environment variables to run the lightweight authentication check. This is a read-only API call. Do not print token values, survey IDs, links, or metadata.
```

Full survey listing is available when explicitly needed:

```bash
python scripts/qualtrics_workflow.py list-surveys
```

## Export Responses

Command:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --survey-id <survey_id> --format csv
```

Prompt alternative:

```text
Export CSV responses for survey id <survey_id> into this repo's ignored raw data folder for survey key my_survey. Do not commit raw data or metadata, and do not print secrets.
```

For Stata/SPSS:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --survey-id <survey_id> --format spss
python scripts/run_analysis.py --survey-key my_survey --mode stata
```

## Analyze Real Local Exports

Command:

```bash
python scripts/run_analysis.py --survey-key my_survey
python scripts/build_slides.py --survey-key my_survey
```

Prompt alternative:

```text
Analyze the newest local Qualtrics export for my_survey, then build the slides. Prefer Stata and Beamer if available; otherwise use Python fallbacks.
```


## Lean Live Validation

Command:

```bash
python scripts/run_live_validation.py --survey-key <survey_key> --survey-name "<survey name>" --spec-file code/<survey_key>/survey_spec.json --n 100 --dry-run
```

Prompt alternative:

```text
Dry-run the live validation helper for this survey. Do not call Qualtrics. Confirm the sequence creates a draft survey, saves the private link locally, prepares synthetic rows, submits them to the Qualtrics test survey, exports once, analyzes once, and builds slides.
```

Use `--export-format spss` for a Stata/SAV validation and the default CSV export for Python-first validation.
