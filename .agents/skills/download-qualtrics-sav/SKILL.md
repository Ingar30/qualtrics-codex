---
name: download-qualtrics-sav
description: Use when the user asks Codex to download Qualtrics responses as an SPSS .sav export for Stata cleaning and figures.
metadata:
  short-description: Download Qualtrics SAV
---

# Download Qualtrics SAV

Use only after the user explicitly asks for a live Qualtrics export.

```bash
python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
```

Prefer saved survey metadata or an explicit `--survey-id`. Keep raw exports under ignored `data/<survey_key>/raw/`. Do not publish raw exports, survey IDs, export metadata, or reusable links.
