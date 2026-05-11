---
title: Repository Smoke Test Survey
subtitle: Qualtrics, Python, Beamer, and native fallback slides
author: Qualtrics Research Workflow Starter
---

# Repository Smoke Test Survey

Qualtrics, Python, Beamer, and native fallback slides

---

## Workflow

1. Write a survey specification in JSON.
2. Create or connect to a Qualtrics survey.
3. Export responses as CSV.
4. Clean and summarize responses with Python.
5. Build Beamer slides when LaTeX is available.
6. Fall back to native Python slides when LaTeX is unavailable.

---

## Analysis Outputs

Run the analysis first:

```bash
python scripts/run_analysis.py --survey-key repo_smoke_test --input tests/fixtures/repo_smoke_test_responses.csv
```

The analysis writes tables and figures to `slides/repo_smoke_test/inputs/`.

---

## Descriptive Summary

{{ include inputs/summary.md }}

---

## Role

![Bar chart of respondent roles.](inputs/role.png)

---

## Workflow Familiarity

![Bar chart of familiarity with reproducible data workflows.](inputs/workflow_familiarity.png)

---

## Preferred Output

![Bar chart of preferred workflow outputs.](inputs/preferred_output.png)

---

## Pipeline Confidence

![Bar chart of confidence running the workflow.](inputs/confidence_running_pipeline.png)

---

## Teaching Point

A useful starter repo should make each survey easy to find, rerun, and explain.

Keep survey-specific code and outputs together, and keep raw data isolated under the survey key.
