# Discrimination Beliefs Example

Paste this into Codex after cloning the repository and installing requirements.

## Live Qualtrics Test Loop

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures.

Use survey_key: discrimination_beliefs
Use survey_name: Discrimination Beliefs Survey
Audience: economics students or researchers

Please:
1. Design a 6-8 question survey that measures perceived prevalence of discrimination in hiring, likely mechanisms, evidence people find persuasive, policy views, and confidence in their answers.
2. Keep question wording neutral and suitable for a classroom or research-methods demonstration.
3. Create the Qualtrics-ready survey spec and the repository's Stata/Python analysis files.
4. Create Beamer slides and native Python/HTML fallback slides.
5. Verify QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values.
6. Ask me before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses.
7. Download the generated Qualtrics responses into the ignored raw data folder.
8. Clean the downloaded data in Stata if available, otherwise Python.
9. Generate summary tables and figures.
10. Compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures.
11. Report the generated artifact paths and note any fallback used.

Do not print secrets, publish raw data, or commit private metadata or reusable links.
```

## Local-Only Smoke Test

Use this version when you do not want Codex to call Qualtrics:

```text
Create a public opinion survey on beliefs about discrimination in hiring. Use survey_key discrimination_beliefs. Generate 100 synthetic responses locally, clean the generated data with Stata if available and Python otherwise, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Do not call the live Qualtrics API.
```

After collecting real responses, you can ask for the local export and rebuild:

```text
Export the real Qualtrics responses for discrimination_beliefs, clean the newest local export in Stata if available and Python otherwise, regenerate figures, and rebuild the slides. Keep raw data, processed real data, metadata, and reusable links private by default.
```
