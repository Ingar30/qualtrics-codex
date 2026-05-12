# Discrimination Beliefs Example

Paste this into Codex after cloning the repository and installing requirements.

## Live Qualtrics Test Loop

```text
Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.

Use survey_key: discrimination_beliefs_demo
Use survey_name: Discrimination Beliefs Survey
Audience: economics students or researchers

Please:
1. Design a 6-8 question survey that measures perceived prevalence of discrimination in hiring, likely mechanisms, evidence people find persuasive, policy views, and confidence in their answers.
2. Keep question wording neutral and suitable for a classroom or research-methods demonstration.
3. Create the Qualtrics-ready survey spec and the repository's Stata/Python analysis files.
4. Create Beamer slides and native Python/HTML fallback slides.
5. Verify QUALTRICS_DATACENTER and QUALTRICS_API_TOKEN are set without printing their values, using check-auth for the first API check.
6. Ask me before creating the draft survey, submitting synthetic responses to Qualtrics, or exporting responses.
7. Prepare 100 synthetic rows for submission to the Qualtrics test survey.
8. Submit the prepared synthetic responses to the Qualtrics test survey.
9. Export the generated Qualtrics responses into the ignored raw data folder.
10. Clean the downloaded data in Stata if available, otherwise Python.
11. Generate summary tables and figures.
12. Save the reusable survey link to ignored local slide inputs without printing it.
13. Compile slides that summarize the workflow, survey design, synthetic response patterns, main figures, and survey link.
14. Report the generated artifact paths and note any fallback used.

Do not print secrets, survey IDs, response IDs, reusable links, raw data, or private metadata.
```

## Local-Only Smoke Test

Use this version when you do not want Codex to call Qualtrics:

```text
Create a public opinion survey on beliefs about discrimination in hiring. Use survey_key discrimination_beliefs_demo. Generate 100 disposable local smoke-test responses, clean the generated data with Stata if available and Python otherwise, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Do not call the live Qualtrics API.
```

After collecting real responses, you can ask for the local export and rebuild:

```text
Export the real Qualtrics responses for discrimination_beliefs_demo, clean the newest local export in Stata if available and Python otherwise, regenerate figures, and rebuild the slides. Keep raw data, processed real data, metadata, IDs, and reusable links private by default.
```
