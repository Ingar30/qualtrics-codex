# Codex Prompt Alternatives

The README is the public entry point and canonical setup sequence. This file only gives prompt variants after the repository is set up.

These are plain-language prompts for the main teaching workflow. Prefer asking Codex what you want; let Codex choose the scripts after it inspects the repository.

Do not paste Qualtrics API tokens into Codex. Store them locally, then ask Codex to verify that the expected environment variables are present without printing values.

## Local Preferences First

Reusable prompt:

```text
Open prompts/configure-local-preferences.md and follow it as instructions for this Codex session. Do not summarize it. Inspect Python, Stata, LaTeX, and Qualtrics environment-variable status first. If Stata, LaTeX, or Qualtrics secrets are missing, tell me where to configure them or which fallback to use. Then ask the needed follow-up questions and save my answers in ignored AGENTS.override.md without secrets.
```

Plain-language version:

```text
Ask me about my local preferences for this Qualtrics workflow before we build anything. First inspect Python, Stata, LaTeX, and Qualtrics environment-variable status without printing secrets. If Stata, LaTeX, or Qualtrics secrets are missing, tell me where to configure them or which fallback to use. Then ask the needed follow-up questions and save my answers in ignored AGENTS.override.md without secrets.
```

## Main Live Teaching Demo

Canonical prompt:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics to test the survey before it is launched to human subjects, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should treat this as a live Qualtrics workflow. It should verify credentials without printing values and ask before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses.

Shorter variant:

```text
Run the main live teaching demo for a discrimination-in-hiring survey. Create the survey in Qualtrics, generate 100 synthetic responses for that survey, submit them through Qualtrics, export once, analyze once, and build slides. Keep credentials, metadata, response IDs, and reusable links private.
```

## When Setup Is Missing

Secrets:

```text
Show me where to store my Qualtrics API token and datacenter outside this repository. Give Windows and macOS/Linux examples. Do not ask me to paste token values into Codex.
```

Stata or LaTeX:

```text
Check whether Stata and LaTeX are discoverable. If Stata is installed but not found, ask me for the executable path and explain STATA_EXE. If LaTeX is not found, continue with native HTML slides unless I ask for help configuring LaTeX.
```

Final local check before sharing:

```text
Use prompts/final-validation-goal.md to validate the public demo. Do not call Qualtrics, do not use secrets, and report any stale docs or private-looking generated output.
```
