# Codex Scaffold Prompt

Use this prompt in Codex after cloning the starter repository.

```text
Create a new Qualtrics research workflow in this repository.

Inputs:
- survey_key: <folder_safe_key>
- survey_name: <human readable survey name>
- topic: <short research or teaching topic>
- audience: <respondents or class context>
- outputs: Python cleaning, summary table, 3-5 simple figures, and native HTML slides

Please:
1. Create code/<survey_key>/survey_spec.json with 4-8 simple questions. Use short snake_case tags. Use "mc" for multiple choice and "text" for one optional open-ended question.
2. Create code/<survey_key>/analysis/run.py modeled on code/repo_smoke_test/analysis/run.py, but adapted to the new question tags and labels.
3. Create slides/<survey_key>/slides.md for scripts/render_slides.py. Use `---` slide separators and read generated figures from slides/<survey_key>/inputs/.
4. Add slides/<survey_key>/inputs/.gitkeep.
5. Do not create or call a live Qualtrics survey unless I explicitly ask.
6. Do not write any API token or secret into the repository.
7. Keep raw data under data/<survey_key>/raw/ and processed data under data/<survey_key>/processed/.
8. After scaffolding, tell me the commands to create the survey, export CSV responses, run analysis, render HTML slides, and optionally export a PDF with `--pdf`.
```

Recommended follow-up after reviewing the scaffold:

```text
Create the live Qualtrics survey from code/<survey_key>/survey_spec.json as a draft, save metadata, and show me the reusable link command. Do not activate it unless I ask.
```
