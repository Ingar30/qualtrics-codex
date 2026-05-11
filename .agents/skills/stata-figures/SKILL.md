---
name: stata-figures
description: Use when the user asks Codex to generate Stata tables and figure PDFs from cleaned Qualtrics data for Beamer slides.
metadata:
  short-description: Build Stata figures
---

# Stata Figures

Use lab-style survey-specific figure scripts when available:

```text
code/<survey_key>/figures/run.do
```

Run through the shared wrapper:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
```

Figure PDFs should go to `slides/<survey_key>/inputs/` for Beamer. PNGs are useful for native HTML fallback slides.
