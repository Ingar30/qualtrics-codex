# Live Validation Goal

Run this only when the user explicitly authorizes live Qualtrics calls.

Use:

```powershell
python scripts/run_live_validation.py --survey-key "<survey_key>" --survey-name "<survey name>" --spec-file "code/<survey_key>/survey_spec.json" --n 100 --i-understand-this-calls-qualtrics
```

Requirements:

- Capture command output instead of printing it.
- Do not print survey IDs, response IDs, reusable links, raw rows, tokens, Qualtrics URLs, or metadata contents.
- Write only sanitized summary metadata under ignored `data/<survey_key>/metadata/`.
- Build analysis outputs plus Beamer/native slide outputs locally.
- Leave Qualtrics cleanup to the user in the Qualtrics UI.
- Use `--export-format spss` for a Stata/SAV validation path and the default CSV export for a Python-first validation path.
- Keep CI, GitHub Pages, and final public validation offline by default.
