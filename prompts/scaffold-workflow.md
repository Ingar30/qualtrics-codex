# Codex Scaffold Prompt

Use this prompt in Codex after cloning the starter repository.

```text
Create a new Qualtrics research workflow in this repository.

Inputs:
- survey_key: <folder_safe_key>
- survey_name: <human readable survey name>
- topic: <short research or teaching topic>
- audience: <respondents or class context>
- outputs: Stata-first cleaning, Python fallback cleaning, summary table, 3-5 simple figures, Beamer slides, and Python fallback slides

Please:
1. Create code/<survey_key>/survey_spec.json with 4-8 simple questions. Use short snake_case tags. Use "mc" for multiple choice and "text" for one optional open-ended question.
2. Create code/<survey_key>/analysis/run.do as the preferred Stata analysis. It should import CSV, write clean.csv, write summary.md and summary.tex, and export each figure as both PDF and PNG under slides/<survey_key>/inputs/.
3. Create code/<survey_key>/analysis/run.py modeled on code/repo_smoke_test/analysis/run.py as the guaranteed Python fallback. It should write the same outputs as the Stata script.
4. Create slides/<survey_key>/main.tex as the preferred Beamer deck. It should read generated summary.tex and figure PDFs from slides/<survey_key>/inputs/.
5. Create slides/<survey_key>/slides.md as the no-install Python fallback deck for scripts/render_slides.py. Use `---` slide separators and the same generated PNG figures from slides/<survey_key>/inputs/.
6. Add slides/<survey_key>/inputs/.gitkeep.
7. Generate a local synthetic response CSV with `python scripts/generate_synthetic_responses.py --survey-key <survey_key> --output build/fixtures/<survey_key>_responses.csv` and use it for the first smoke test.
8. Do not create or call a live Qualtrics survey unless I explicitly ask.
9. Do not write any API token or secret into the repository.
10. Keep raw data under data/<survey_key>/raw/ and processed data under data/<survey_key>/processed/.
11. Do not add Quarto, R, Node, Jinja2, YAML, or new slide dependencies unless I explicitly ask for that extension.
12. After scaffolding, tell me the commands to generate synthetic responses, run analysis with `python scripts/run_analysis.py --survey-key <survey_key> --input build/fixtures/<survey_key>_responses.csv`, build slides with `python scripts/build_slides.py --survey-key <survey_key>`, create the live survey, and export CSV responses.
```

Recommended follow-up after reviewing the scaffold:

```text
Create the live Qualtrics survey from code/<survey_key>/survey_spec.json as a draft, save metadata, and show me the reusable link command. Do not activate it unless I ask.
```

Optional follow-up for Python-only users:

```text
Force the no-install slide path with `python scripts/build_slides.py --survey-key <survey_key> --mode python` and check the HTML output.
```
