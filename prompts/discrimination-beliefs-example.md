# Discrimination Beliefs Example

Paste this into Codex after cloning the repository and installing requirements.

```text
Create a Qualtrics survey workflow on beliefs about discrimination in hiring and wage setting.

Use survey_key: discrimination_beliefs
Use survey_name: Discrimination Beliefs Survey
Audience: economics students or researchers

Please:
1. Design a 6-8 question survey that measures perceived prevalence of discrimination, likely mechanisms, evidence people find persuasive, policy views, and confidence in their answers.
2. Keep question wording neutral and suitable for a classroom or research-methods demonstration.
3. Create the Qualtrics-ready survey spec and the repository's Stata/Python analysis files.
4. Create Beamer slides and native Python/HTML fallback slides.
5. Generate 100 synthetic responses locally.
6. Clean the generated data in Stata if available, otherwise Python.
7. Generate summary tables and figures.
8. Compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures.
9. Report the generated artifact paths and note any fallback used.

Do not call the live Qualtrics API unless I explicitly ask. Do not create a live survey, print secrets, publish raw data, or commit private metadata.
```

After reviewing the synthetic workflow, you can ask for a live draft/test link:

```text
Create the live Qualtrics survey as a draft from code/discrimination_beliefs/survey_spec.json and show me how to retrieve the reusable test link. Verify QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values. Do not activate the survey unless I ask.
```

After collecting real responses, you can ask for the local export and rebuild:

```text
Export the real Qualtrics responses for discrimination_beliefs, clean the newest local export in Stata if available and Python otherwise, regenerate figures, and rebuild the slides. Keep raw data, processed real data, metadata, and reusable links private by default.
```
