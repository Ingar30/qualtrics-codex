# Full Loop Survey Prompt

Use this prompt when you want Codex to go from a survey idea to tested outputs.

```text
Create a Qualtrics survey workflow from this idea:

<describe the survey topic, target audience, and what you want to learn>

Use survey_key: <folder_safe_key>
Use survey_name: <human readable survey name>

Please:
1. Turn the idea into a simple 4-8 question survey spec.
2. Create the Stata-first analysis and Python fallback analysis.
3. Create Beamer slides and native Python/HTML fallback slides.
4. Generate 100 synthetic responses locally.
5. Clean the synthetic responses in Stata if available, otherwise Python.
6. Generate tables and figures.
7. Compile slides with a short description of the survey and the response patterns.
8. Tell me what command I would run later to create a live draft survey, get a test link, and export real responses.

Do not call the live Qualtrics API unless I explicitly ask. Do not print or store secrets. Keep raw real data, processed real data, survey metadata, and reusable survey links private by default.
```

Short version:

```text
Generate 100 synthetic responses, clean them in Stata or Python, generate figures, and compile slides with a description of the survey and responses. Use the repository's Qualtrics workflow and do not call the live API unless I explicitly ask.
```
