---
name: get-survey-link
description: Use when the user asks Codex to retrieve or save the reusable anonymous Qualtrics link for a local survey workflow.
metadata:
  short-description: Get survey link
---

# Get Survey Link

Use only after the user explicitly asks for a live Qualtrics link action.

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key>
```

By default, the command saves the reusable link to ignored local metadata without printing it. Use `--show-private-link` only when the user needs to see the link in the local terminal. Never commit or publish reusable links by default.

If the user asks to include the link in local slides, use:

```bash
python scripts/qualtrics_workflow.py get-link --survey-key <survey_key> --write-slide-inputs
```

This writes ignored `slides/<survey_key>/inputs/survey_link.tex` and `slides/<survey_key>/inputs/survey_link.md` files without printing the link.
