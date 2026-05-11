# Start With Codex

Paste this into Codex after cloning `https://github.com/Ingar30/qualtrics-codex` and opening the repository folder.

```text
Inspect README.md, AGENTS.md, pyproject.toml, requirements.txt, scripts/, code/repo_smoke_test/, slides/repo_smoke_test/, tests/, docs/, site/, and .github/workflows/.

I want to create a new Qualtrics research workflow in this repo.

Inputs:
- survey_key: <folder_safe_key>
- survey_name: <human readable survey name>
- topic: <short research or teaching topic>
- audience: <respondents or class context>

Please scaffold the workflow using the repository's existing patterns:
1. Create code/<survey_key>/survey_spec.json with 4-8 simple questions.
2. Create Stata-first analysis in code/<survey_key>/analysis/run.do.
3. Create the Python fallback in code/<survey_key>/analysis/run.py.
4. Create Beamer slides in slides/<survey_key>/main.tex.
5. Create native Python/HTML fallback slides in slides/<survey_key>/slides.md.
6. Generate synthetic responses into build/fixtures/<survey_key>_responses.csv.
7. Run analysis against the synthetic responses.
8. Build slides.
9. Explain where I should store local Qualtrics API keys before any live API call.
10. Report the exact commands I should run next for live Qualtrics export.

Safety rules:
- Do not call the live Qualtrics API unless I explicitly ask.
- Do not create, activate, modify, or delete a live survey unless I explicitly ask.
- Do not print or store API tokens.
- Do not commit raw data, processed real data, survey metadata, or reusable survey links.
- Keep secrets outside the repository, preferably in $HOME/.secrets/qualtrics.env.ps1 on Windows or $HOME/.secrets/qualtrics.env on macOS/Linux.
- If checking secrets, verify only that QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set; never print their values.
- Prefer Stata and Beamer when available, but fall back to Python and native HTML slides if they are missing.

Also show me prompt alternatives from docs/codex-prompt-alternatives.md for any command I am likely to run next.
```
