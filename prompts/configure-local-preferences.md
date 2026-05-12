# Configure Local Preferences

Use this prompt after cloning the repository, before asking Codex to build the first real workflow. It is optional. If you skip it, Codex should use the repository defaults.

```text
Before we scaffold survey workflows in this repository, ask me how I want Codex to operate locally.

Please ask short questions covering:

1. Analysis stack:
   - Stata-first when available, with Python fallback.
   - Python-only.

2. Qualtrics export format:
   - If I choose Stata, use SPSS/SAV exports and Stata import with `import spss`.
   - If I choose Python, use CSV exports and Python analysis.

3. Slide stack:
   - Beamer-first when available, with native Markdown/HTML fallback.
   - Native Markdown/HTML only.

4. Live API behavior:
   - Local synthetic smoke tests first, no Qualtrics calls until I explicitly ask.
   - Live draft/test surveys are allowed only after explicit confirmation.

5. Public/private boundary:
   - Keep new code/<survey_key>/ and slides/<survey_key>/ folders ignored unless I explicitly promote them.
   - Keep raw exports, processed real data, metadata, and reusable links private by default.

After I answer, update AGENTS.override.md with my local preferences. Do not store secrets, API tokens, survey IDs, response IDs, or reusable links there.

If I do not answer, proceed with the simplest default setup: Stata-first if available, Python fallback, CSV for Python workflows, SAV for Stata workflows, Beamer-first with native fallback, local synthetic smoke tests first, and public GitHub Pages synthetic-only.
```

Suggested `AGENTS.override.md` shape:

```markdown
# Local Workflow Preferences

- Analysis: Stata-first with Python fallback.
- Qualtrics export: SAV/SPSS for Stata workflows; CSV for Python workflows.
- Slides: Beamer-first with native Markdown/HTML fallback.
- Live API: local synthetic smoke tests first; ask before every live Qualtrics mutation/export.
- Public/private: keep ad hoc survey folders and all live artifacts ignored unless explicitly promoted.
```
