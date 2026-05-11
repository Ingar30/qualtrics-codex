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

## Scaffold A New Workflow

Prompt:

```text
Create a new Qualtrics research workflow using prompts/start-with-codex.md. Use survey_key <survey_key>, survey_name <survey_name>, topic <topic>, and audience <audience>. Generate synthetic responses and run the first smoke test. Do not call the live Qualtrics API.
```

## Full Survey-To-Slides Loop

Prompt:

```text
Create a survey from this broad idea: <idea>. Use survey_key <survey_key>. Generate 100 synthetic responses, clean them in Stata or Python depending on what is available, generate figures, and compile slides with a description of the survey and the response patterns. Do not call the live Qualtrics API unless I explicitly ask.
```

Prompt for a live test link:

```text
Create the live Qualtrics survey as a draft and show me how to get the reusable test link. Verify QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values. Do not activate the survey unless I ask.
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
Run the repository smoke test without calling Qualtrics: generate synthetic responses for repo_smoke_test, analyze them, and build the slides. If Stata or LaTeX is missing, use the repository fallbacks.
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
python scripts/qualtrics_workflow.py list-surveys
```

Prompt alternative:

```text
Use the local Qualtrics environment variables to list my surveys. This is a read-only API call. Do not print any token values.
```

## Export Responses

Command:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --survey-id SV_... --format csv
```

Prompt alternative:

```text
Export CSV responses for survey id SV_... into this repo's ignored raw data folder for survey key my_survey. Do not commit raw data or metadata, and do not print secrets.
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
