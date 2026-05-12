# Configure Local Preferences

Use this prompt after cloning the repository, before asking Codex to build the first real workflow. It is optional. If you skip it, Codex should use the repository defaults.

```text
Before we scaffold survey workflows in this repository, ask me how I want Codex to operate locally.

First, inspect the local environment without changing files or calling Qualtrics:

- Check that Python and the repository dependencies are available.
- Check whether Stata is discoverable through `STATA_EXE`, PATH, or common local install paths.
- Check whether LaTeX/Beamer tools are discoverable, especially `latexmk`, `xelatex`, and `pdflatex`.
- Check only whether `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` are set; do not print their values.
- If Qualtrics keys are missing, point me to `docs/local-qualtrics-secrets.md` and `$HOME\.secrets\qualtrics.env.ps1` on Windows or `$HOME/.secrets/qualtrics.env` on macOS/Linux. Do not ask me to paste secrets into Codex.

Then ask short questions covering:

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
   - Local smoke tests only when needed to check analysis and slides without credentials.
   - Live draft/test surveys and Qualtrics synthetic response submission are allowed only after explicit confirmation.

5. Public/private boundary:
   - Keep new code/<survey_key>/ and slides/<survey_key>/ folders ignored unless I explicitly promote them.
   - Keep raw exports, processed real data, metadata, and reusable links private by default.

After I answer, update AGENTS.override.md with my local preferences. Do not store secrets, API tokens, survey IDs, response IDs, or reusable links there.

If Stata or LaTeX is missing, ask whether to continue with Python/native fallbacks or help configure the local executable path. If I do not answer, proceed with the simplest default setup: Stata-first if available, Python fallback, CSV for Python workflows, SAV for Stata workflows, Beamer-first with native fallback, local synthetic smoke tests only when useful, Qualtrics-submitted synthetic responses for live demos, and public GitHub Pages synthetic-only.
```

Suggested `AGENTS.override.md` shape:

```markdown
# Local Workflow Preferences

- Analysis: Stata-first with Python fallback.
- Qualtrics export: SAV/SPSS for Stata workflows; CSV for Python workflows.
- Slides: Beamer-first with native Markdown/HTML fallback.
- Live API: local smoke tests only when needed; ask before every live Qualtrics mutation/export, including synthetic response submission.
- Public/private: keep ad hoc survey folders and all live artifacts ignored unless explicitly promoted.
```
