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
5. Codex generates or downloads responses.
6. Codex cleans the data with Stata when available and Python otherwise.
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
python scripts/qualtrics_workflow.py create-survey --survey-key <survey_key> --survey-name "<survey_name>" --spec-file code/<survey_key>/survey_spec.json
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key>
```

Do not activate a survey unless the user explicitly asks.

## Real Response Mode

Export real responses only after the user explicitly asks for a live Qualtrics export:

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --survey-id SV_... --format csv
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

Raw exports, processed real data, Qualtrics metadata, survey IDs, and reusable links stay private by default.

Qualtrics CSV exports often contain two metadata rows after the header. Cleaning scripts should filter those out when `ResponseId` is present by keeping real response IDs that start with `R_`.

Draft or inactive surveys may still accept API-created test responses. Do not treat inactive status as a protection against API mutations.

## Typical Prompt

```text
Generate 100 synthetic responses, download the responses, clean them in Stata or Python, generate figures, and compile slides with a description of the survey and the responses.
```

In this repository, Codex should interpret that as:

- generate local synthetic responses unless the user explicitly asks for live API submission or export;
- use Stata if available, otherwise Python;
- generate both PDF and PNG figures;
- compile Beamer slides if available, otherwise native HTML slides;
- report the files created and any fallback used.
