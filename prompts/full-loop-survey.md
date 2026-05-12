# Full Loop Survey Prompt

Use this prompt when you want Codex to go from a survey idea to tested outputs.

```text
Create a Qualtrics survey workflow from this idea:

<describe the survey topic, target audience, and what you want to learn>

Use survey_key: <folder_safe_key>
Use survey_name: <human readable survey name>

Please:
1. Turn the idea into a simple 4-8 question survey spec.
2. Create lab-style Stata cleaning/figure scripts when appropriate, plus the Python fallback analysis.
3. Create Beamer slides and native Python/HTML fallback slides.
4. Generate 100 disposable local smoke-test responses only to check the analysis and slide path.
5. Clean the smoke-test responses in Stata if available, otherwise Python.
6. Generate tables and figures.
7. Compile slides with a short description of the survey and the response patterns.
8. If I choose Stata, plan for SPSS/SAV export and Stata import. If I choose Python, plan for CSV export and Python analysis.
9. Tell me what command I would run later to check auth, create a live draft survey, submit synthetic responses to a test survey, get a test link, and export real responses.

Do not call the live Qualtrics API unless I explicitly ask. Do not print or store secrets. Keep raw real data, processed real data, survey metadata, and reusable survey links private by default.
```

Canonical live-test version:

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.
```

Use this only when you want a live Qualtrics test loop. Codex should verify credentials without printing them, use `check-auth` for the first API check, and ask before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses. The lean live path saves the reusable link to ignored slide inputs with `get-link --write-slide-inputs`, prepares synthetic rows, submits them to the Qualtrics test survey, exports once, analyzes once, and builds slides.
For Stata workflows, export SPSS/SAV and import with Stata. For Python workflows, export CSV and analyze with Python.

Local-only version:

```text
Create a public opinion survey on beliefs about discrimination in hiring. Use survey_key discrimination_beliefs_demo. Generate 100 disposable local smoke-test responses, clean the generated data with Stata if available and Python otherwise, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Do not call the live Qualtrics API.
```
