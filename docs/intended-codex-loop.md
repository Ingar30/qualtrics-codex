# Intended Codex Loop

This repository is designed for a conversational workflow, not only for manual commands.

The intended user experience is:

1. A researcher asks Codex for a survey. The request can be detailed or broad.
2. Codex turns the idea into a `survey_spec.json`, analysis scripts, and slide files.
3. Codex decides whether it has enough information to proceed. It asks only when the answer changes live API use, privacy, or core survey design.
4. Codex asks or infers the run mode:
   - synthetic-only local test;
   - live draft/test link;
   - export/download existing real responses.
   - live synthetic response submission for a test survey.
5. Codex generates or downloads responses.
6. Codex cleans the data with lab-style Stata cleaning/figures when available and Python otherwise.
7. Codex generates figures and tables.
8. Codex compiles Beamer slides when available and native HTML slides otherwise.
9. Codex reports the outputs and keeps private artifacts private.

## Default Mode

Default to a synthetic local test. This validates the full analysis and slide path without Qualtrics credentials:

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

For a new live survey, submit one synthetic response first, export and inspect it locally, then submit the rest without duplicating row 1:

```bash
python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --limit 1
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv --resume
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Use `--smoke-then-rest` only when the user explicitly wants to submit all synthetic rows in one command. Response IDs are saved only in ignored local metadata.

## Real Response Mode

Export real responses only after the user explicitly asks for a live Qualtrics export:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id SV_... --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

For the Stata/SPSS path:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
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
- submit one synthetic response first, export/check locally, then continue with `--resume`;
- download the generated response export into ignored raw data folders;
- filter Qualtrics CSV metadata rows by keeping `ResponseId` values that start with `R_` when that column exists;
- clean with Stata if available, otherwise Python;
- generate both PDF and PNG figures;
- compile Beamer slides if available, otherwise native HTML slides;
- report the files created and any fallback used.

For a no-credentials smoke test, ask Codex to generate the 100 synthetic responses locally rather than on Qualtrics.
