---
name: beamer-slides
description: Compile or inspect Beamer slide output for a survey workflow, using generated tables and figure PDFs when available and native slides as fallback when LaTeX is unavailable.
metadata:
  short-description: Build Beamer slides
---

# Beamer Slides

Use this when the user asks to build or inspect final PDF slides for a survey workflow.

## Workflow

Preferred generic command:

```bash
python scripts/build_slides.py --survey-key <survey_key> --mode auto
```

Force Beamer:

```bash
python scripts/build_slides.py --survey-key <survey_key> --mode beamer
```

Force the native fallback:

```bash
python scripts/build_slides.py --survey-key <survey_key> --mode python
```

Windows compatibility wrapper:

```powershell
.\scripts\build-slides.ps1 -SurveyKey "<survey_key>"
```

## Expected Inputs

- `slides/<survey_key>/main.tex` for Beamer.
- `slides/<survey_key>/slides.md` for native HTML/PDF fallback.
- Generated tables, figures, and optional private link inputs under `slides/<survey_key>/inputs/`.

Use `\IfFileExists` in Beamer decks so slides can compile before analysis inputs exist. Reusable Qualtrics links belong in ignored `inputs/survey_link.tex` and `inputs/survey_link.md`, not in tracked source.

## Safety

- Do not call Qualtrics while compiling slides.
- Do not edit raw data.
- Do not print or publish private survey links.
- If figures look stale, rerun analysis and rebuild slides.
