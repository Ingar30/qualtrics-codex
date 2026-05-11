---
name: beamer-slides
description: Use when the user asks Codex to compile survey slides to PDF with LaTeX/Beamer, falling back to native Python/HTML slides when needed.
metadata:
  short-description: Compile Beamer slides
---

# Beamer Slides

Compile slides with:

```bash
python scripts/build_slides.py --survey-key <survey_key>
```

The wrapper tries Beamer first and writes `build/slides/<survey_key>/slides.pdf` when LaTeX works. If LaTeX is missing or fails, it renders native HTML slides and a browser PDF when Chrome, Edge, or Chromium is available.

On Windows, the PowerShell wrapper is:

```powershell
.\scripts\build-slides.ps1 -SurveyKey <survey_key>
```
