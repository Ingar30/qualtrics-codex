# Start With Codex

Paste this into Codex after cloning `https://github.com/Ingar30/qualtrics-codex` and opening the repository folder.

```text
Inspect README.md, AGENTS.md, pyproject.toml, requirements.txt, scripts/, code/repo_smoke_test/, slides/repo_smoke_test/, tests/, docs/, site/, and .github/workflows/.

I want to create a new Qualtrics research workflow in this repo.

Inputs:
- survey_key: <folder_safe_key>
- survey_name: <human readable survey name>
- topic: <short research or teaching topic, or a broad idea Codex should turn into a survey>
- audience: <respondents or class context>

Please scaffold the workflow using the repository's existing patterns:
0. If this is my first workflow here, offer to use `prompts/configure-local-preferences.md`. If I do not answer, proceed with the repository defaults.
1. Confirm dependencies are installed, or tell me to run `.\scripts\setup.ps1` on Windows.
2. Create code/<survey_key>/survey_spec.json with 4-8 simple questions.
3. For Stata-first workflows, create code/<survey_key>/cleaning/run.do and code/<survey_key>/figures/run.do; for compact workflows, code/<survey_key>/analysis/run.do is acceptable.
4. Create the Python fallback in code/<survey_key>/analysis/run.py.
5. Create Beamer slides in slides/<survey_key>/main.tex.
6. Create native Python/HTML fallback slides in slides/<survey_key>/slides.md.
7. Ask or infer whether I want a quick local smoke test, a live Qualtrics test survey with synthetic response submission, or export/download of existing real responses.
8. Unless I explicitly ask for a live Qualtrics action, generate disposable smoke-test responses into build/fixtures/<survey_key>_responses.csv only to check analysis and slides.
9. Run analysis against the smoke-test responses.
10. Build slides.
11. Explain where I should store local Qualtrics API keys before any live API call.
12. Report the exact commands I should run next for check-auth, live draft creation, live synthetic response submission, live export, analysis, and slides.

Safety rules:
- Do not call the live Qualtrics API unless I explicitly ask.
- Do not create, activate, modify, or delete a live survey unless I explicitly ask.
- Do not print or store API tokens.
- Do not commit raw data, processed real data, survey metadata, or reusable survey links.
- Keep secrets outside the repository, preferably in $HOME/.secrets/qualtrics.env.ps1 on Windows or $HOME/.secrets/qualtrics.env on macOS/Linux.
- If checking secrets, verify only that QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set; never print their values.
- Prefer Stata and Beamer when available, but fall back to Python and native HTML slides if they are missing.
- If I choose Stata, export/download Qualtrics responses as SPSS/SAV and import with Stata. If I choose Python, export/download responses as CSV and analyze with Python.
- For live synthetic response submission, use the lean path by default: create the survey in Qualtrics, prepare synthetic rows, submit them to the Qualtrics test survey, export once, analyze once, and build slides.
- If analyzing a Qualtrics CSV export, filter out metadata rows by keeping rows where ResponseId starts with R_ when that column exists.

Also show me prompt alternatives from docs/codex-prompt-alternatives.md for any command I am likely to run next.
```
