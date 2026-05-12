# Configure Local Preferences

```text
You are being given this file as an instruction prompt for the current Codex session.

Do not summarize, explain, or quote this file back to me. Follow it now.

Goal: inspect whether this machine is ready for the Qualtrics-to-analysis-to-slides teaching workflow, then ask me only the follow-up questions needed to choose local defaults.

First, inspect the local environment without changing files and without calling Qualtrics:

- Check that Python and the repository dependencies are available.
- Check whether Stata is discoverable through `STATA_EXE`, PATH, or common install paths.
- If Stata is not found, ask whether I have Stata installed and where the executable is. Mention that on Windows it often looks like `C:\Program Files\Stata19\StataMP-64.exe`, and that the path can be supplied with `STATA_EXE`.
- Check whether LaTeX/Beamer tools are discoverable, especially `latexmk`, `xelatex`, and `pdflatex`.
- Check only whether `QUALTRICS_DATACENTER` and `QUALTRICS_API_TOKEN` are set; do not print their values.
- If Qualtrics keys are missing, always tell me where to put and load them: `docs/local-qualtrics-secrets.md`, `$HOME\.secrets\qualtrics.env.ps1` on Windows, or `$HOME/.secrets/qualtrics.env` on macOS/Linux. Ask whether I want help creating or loading that local file. Do not ask me to paste secrets into Codex.

Then report a short environment status summary with no secret values.

Then ask short questions covering only what is needed:

1. Analysis stack:
   - Stata-first when available, with Python fallback.
   - Python-only.
   - If Stata was not found, ask whether to continue with Python fallback or help locate Stata.

2. Qualtrics export format:
   - If I choose Stata, use SPSS/SAV exports and Stata import with `import spss`.
   - If I choose Python, use CSV exports and Python analysis.

3. Slide stack:
   - Beamer-first when available, with native Markdown/HTML fallback.
   - Native Markdown/HTML only.

4. Live API behavior:
   - Local smoke tests only when needed to check analysis and slides without credentials.
   - For the main live teaching demo, create the survey in Qualtrics and submit Codex-generated synthetic responses to Qualtrics only after explicit confirmation.

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
