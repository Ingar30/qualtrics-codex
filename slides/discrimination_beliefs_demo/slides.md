---
title: Beliefs About Discrimination in Hiring
subtitle: Synthetic Qualtrics workflow demo
author: qualtrics-codex
---

# Beliefs About Discrimination in Hiring

Synthetic Qualtrics workflow demo

---

## Workflow

1. Design a neutral public opinion survey.
2. Generate synthetic responses locally or submit them to Qualtrics after approval.
3. Export responses from Qualtrics into an ignored raw folder.
4. Clean the data with Stata when available, otherwise Python.
5. Build figures and slides from reproducible local outputs.

---

## Survey Design

The demo asks about perceived prevalence, likely mechanisms, persuasive evidence, policy responses, and confidence.

Only synthetic/demo outputs are public by default.

---

## Synthetic Response Summary

{{ include inputs/summary.md }}

---

## Perceived Prevalence

![Bar chart of perceived prevalence of discrimination in hiring.](inputs/prevalence_discrimination.png)

---

## Likely Mechanisms

![Bar chart of perceived mechanisms behind discrimination in hiring.](inputs/main_mechanism.png)

---

## Persuasive Evidence

![Bar chart of evidence respondents find persuasive.](inputs/persuasive_evidence.png)

---

## Policy Response

![Bar chart of preferred policy responses.](inputs/policy_response.png)

---

## Confidence

![Bar chart of confidence in survey answers.](inputs/confidence.png)

---

## Public Boundary

Publish the synthetic slides, tables, and figures. Keep survey specs, raw exports, processed real data, response IDs, reusable links, and metadata private unless explicitly promoted.
