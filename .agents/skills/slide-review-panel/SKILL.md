---
name: slide-review-panel
description: Review a built survey slide deck for data integrity, slide design, and teaching narrative issues, using subagents only when the user explicitly asks for a parallel review panel.
metadata:
  short-description: Review survey slides
---

# Slide Review Panel

Use this after slides have been built with:

```bash
python scripts/build_slides.py --survey-key <survey_key>
```

## Review Lenses

- Data integrity: tables, figures, labels, sample size, and consistency with `survey_spec.json`, generated inputs, and visible slide claims.
- Slide design: readability, layout, figure sizing, title/body balance, and presentation polish.
- Teaching narrative: whether the deck clearly explains survey creation, response collection, analysis, figures, and slide output.

If the user explicitly asks for subagents or a parallel review panel, run the three lenses independently and synthesize the findings. Otherwise, perform the same three-lens review locally.

## Output

Lead with concrete issues, ordered by severity. Include slide/page references where possible, evidence from the PDF/source/inputs/logs, and suggested fixes. Separate required fixes from optional polish.

## Safety

- Do not call Qualtrics during review.
- Do not regenerate responses during review.
- Do not edit `data/<survey_key>/raw/`.
- If the PDF or HTML deck does not exist, build or ask to build it before guessing at slide contents.
