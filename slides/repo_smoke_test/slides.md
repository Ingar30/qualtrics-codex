---
title: Repository Offline Check Survey
subtitle: Qualtrics, Python, Beamer, and native fallback slides
author: Qualtrics Research Workflow Starter
---

# Repository Offline Check Survey

Qualtrics, Python, Beamer, and native fallback slides

---

## Workflow

1. Ask Codex for local workflow preferences.
2. Scaffold a survey specification and analysis files.
3. Use disposable local rows only for offline checks.
4. Submit synthetic rows through Qualtrics for live demos.
5. Build Beamer slides when LaTeX is available.
6. Fall back to native slides when LaTeX is unavailable.

---

## Analysis Outputs

Codex should run the local offline check only to confirm that cleaning, figures, tables, and slides build.

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
