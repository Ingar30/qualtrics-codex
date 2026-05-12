# Intended Codex Loop

This repository is designed for a conversational workflow, not only for manual commands.

The intended user experience is:

1. A researcher starts with local preferences, either by using `prompts/configure-local-preferences.md` or by asking Codex to ask about Stata/Python, export, slide, and live-API preferences.
2. The researcher asks Codex for a survey. The request can be detailed or broad.
3. Codex turns the idea into a `survey_spec.json`, analysis scripts, and slide files.
4. Codex decides whether it has enough information to proceed. It asks only when the answer changes live API use, privacy, or core survey design.
5. Codex asks or infers the run mode:
   - quick local smoke test;
   - live Qualtrics test survey with synthetic response submission;
   - export/download existing real responses.
6. Codex generates or downloads responses.
7. Codex cleans the data with lab-style Stata cleaning/figures when available and Python otherwise.
8. Codex generates figures and tables.
9. Codex compiles Beamer slides when available and native HTML slides otherwise.
10. Codex reports the outputs and keeps private artifacts private.

On first use, Codex can ask the optional preference questions in `prompts/configure-local-preferences.md` and write the answers to ignored `AGENTS.override.md`. If the user does not answer, Codex should proceed with the defaults: Stata-first when available, Python fallback, Beamer-first with native fallback, local synthetic smoke tests only when needed, Qualtrics-submitted synthetic responses for live demos, public Pages synthetic-only.

When the user chooses Stata, live exports should use SPSS/SAV and Stata should import with `import spss`. When the user chooses Python, live exports should use CSV and Python analysis should filter Qualtrics metadata rows when `ResponseId` is available.

## Default Mode

Use a local synthetic smoke test only to validate the analysis and slide path without Qualtrics credentials:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/build_slides.py --survey-key <survey_key>
```

## Live Test Link Mode

A live draft survey and reusable test link require explicit user approval and local Qualtrics secrets:

```bash
python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
```

`--write-slide-inputs` writes ignored local link inputs for Beamer/native slides without printing the link. Do not activate a survey or publish reusable links unless the user explicitly asks.

## Live Synthetic Response Mode

For a new live test survey, keep the default path lean: create the survey in Qualtrics, prepare synthetic rows, submit them to the Qualtrics test survey, export once, analyze once, then build slides.

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Response IDs are saved only in ignored local metadata and are not printed.

## Real Response Mode

Export real responses only after the user explicitly asks for a live Qualtrics export:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id <survey_id> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

For the Stata/SPSS path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
python scripts/build_slides.py --survey-key <survey_key>
```

For the Python/CSV path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key> --mode python
python scripts/build_slides.py --survey-key <survey_key>
```

Raw exports, processed real data, Qualtrics metadata, survey IDs, and reusable links stay private by default.

Qualtrics CSV exports often contain two metadata rows after the header. Cleaning scripts should filter those out when `ResponseId` is present by keeping real response IDs that start with `R_`.

Draft or inactive surveys may still accept API-created test responses. Do not treat inactive status as a protection against API mutations.

## Canonical Prompt

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should interpret that as a live Qualtrics test loop:

- design a neutral 6-8 question public-opinion survey and save the spec under a folder-safe `survey_key`;
- verify `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` are set without printing values;
- use `check-auth` for the first read-only API check instead of listing every survey;
- ask before creating a live draft survey, submitting synthetic responses to Qualtrics, or exporting responses;
- save the reusable link to ignored metadata and, if slides should include it, ignored slide inputs;
- submit generated synthetic rows to the test survey in one step;
- download the generated response export into ignored raw data folders;
- filter Qualtrics CSV metadata rows by keeping `ResponseId` values that start with `R_` when that column exists;
- clean with Stata if available, otherwise Python;
- generate both PDF and PNG figures;
- compile Beamer slides if available, otherwise native HTML slides;
- report the files created and any fallback used.

For a no-credentials smoke test, ask Codex to generate disposable local responses only to check analysis and slides.

## Recent Live Prompt Validation

On May 12, 2026, the repository command loop was validated locally with the labor-market/immigration prompt:

```text
Create a public opinion survey on labor market concerns and support for immigration in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

The run created a live test survey, submitted 100 synthetic responses, exported and analyzed the responses, generated figures, and built slides. Only this sanitized fact should be public; live identifiers, response IDs, reusable links, raw rows, export paths, and metadata contents stay local.
