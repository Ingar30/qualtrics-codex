# Final Validation Goal Prompt

Use this as a final `/goal` prompt before sharing the repository publicly. If `/goal` is not available in your Codex interface, paste it as a normal Codex prompt.

```text
Prepare this repository for public sharing as a Qualtrics-to-analysis-to-slides starter workflow.

Do a fresh inspection of README.md, AGENTS.md, pyproject.toml, requirements.txt, scripts/, code/, slides/, tests/, docs/, site/, and .github/workflows/.

Validate that:
1. README instructions are enough for a new researcher to clone the repo, open it in Codex, set local preferences, and run the main live teaching demo;
2. no live Qualtrics API call is required for tests, Pages, or public demo artifacts;
3. secrets are documented as local-only and are not committed;
4. raw Qualtrics exports, processed real data, metadata, and survey links stay private by default;
5. Stata and Beamer are preferred when available, but Python analysis and native HTML slides work as fallbacks;
6. GitHub Pages builds only synthetic discrimination-beliefs demo artifacts;
7. synthetic responses are framed as Qualtrics-submitted demo responses, with local CSVs used only for staging or offline checks;
8. Stata examples use SPSS/SAV export and Stata import, while Python examples use CSV export and Python analysis;
9. local preferences are documented with ignored AGENTS.override.md and no secrets;
10. there are no stale references to deleted starter prompts or older multi-workflow examples.

Run the shortest appropriate validation commands, including pytest and the synthetic site build. Do not call the live Qualtrics API. Do not expose secrets. Report any remaining blockers, then give the exact next commands for a user who wants to run the workflow locally.
```
