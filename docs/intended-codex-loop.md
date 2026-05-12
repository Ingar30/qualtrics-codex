# Intended Codex Loop

The intended user experience is intentionally narrow:

1. The researcher asks Codex to inspect local preferences with `prompts/configure-local-preferences.md`.
2. Codex checks Python, Stata, LaTeX/Beamer, and Qualtrics environment-variable presence without printing secrets.
3. The researcher gives the main live teaching prompt.
4. Codex creates or updates a survey spec, analysis files, and slide files.
5. Codex asks before each live Qualtrics action: create survey, submit synthetic responses, export responses, or retrieve a reusable link.
6. Codex generates synthetic rows for the created survey, submits them through Qualtrics, exports once, analyzes once, and builds slides.
7. Codex reports artifact paths and keeps private identifiers, raw exports, metadata, and reusable links out of git.

## Main Prompt

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics to test the survey before it is launched to human subjects, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Codex should interpret that as a live Qualtrics test loop:

- design a neutral 6-8 question public-opinion survey and save the spec under a folder-safe `survey_key`;
- verify `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` are set without printing values;
- use `check-auth` for the first read-only API check;
- ask before creating a live draft survey, submitting synthetic responses to Qualtrics, exporting responses, or saving a reusable link;
- save the reusable link to ignored metadata and, if slides should include it, ignored slide inputs;
- submit generated synthetic rows to the test survey in one step;
- download the generated response export into ignored raw data folders;
- filter Qualtrics CSV metadata rows by keeping `ResponseId` values that start with `R_` when that column exists;
- clean with Stata if available and configured, otherwise Python;
- compile Beamer slides if available, otherwise native HTML slides;
- report created files and any fallback used.

## Defaults

When preferences are unclear, Codex should use the simplest working path: Stata-first when available, Python fallback, Beamer-first with native HTML fallback, SAV/SPSS for Stata workflows, CSV for Python workflows, and Qualtrics-submitted synthetic responses for live demos.

Local synthetic CSVs are only supporting files. They are useful for offline checks or as staging files before submission to Qualtrics; they are not the demo object of interest.

## Public Boundary

GitHub Pages and CI do not call Qualtrics and do not need Qualtrics secrets. Public artifacts are generated from synthetic fixture data only. Raw exports, processed real data, survey IDs, response IDs, export metadata, reusable links, and API tokens stay local by default.
