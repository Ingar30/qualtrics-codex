---
name: slide-review-panel
description: Use when the user asks Codex to review a built survey slide PDF for data integrity, slide design, and teaching narrative before presenting.
metadata:
  short-description: Review slide PDF
---

# Slide Review Panel

Use after a deck exists under:

```text
build/slides/<survey_key>/slides.pdf
```

Review from three perspectives:

1. Data integrity: sample size, labels, tables, figures, and consistency with the survey spec.
2. Slide design: readability, figure sizing, visual hierarchy, and PDF quality.
3. Teaching narrative: whether the deck clearly explains workflow, survey design, response patterns, and main figures.

Return concrete findings and suggested fixes. Do not regenerate data, call Qualtrics, or edit raw exports unless explicitly asked.
