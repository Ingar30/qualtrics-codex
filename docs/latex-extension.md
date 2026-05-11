# LaTeX And Beamer Extension

The default starter workflow uses Quarto RevealJS slides because they render to HTML without a TeX installation. Use this extension if you prefer Beamer or PDF slides.

## Option 1: Quarto To Beamer

Quarto can render Beamer when a LaTeX distribution is installed.

Create a `.qmd` file with:

```yaml
---
title: "Survey Results"
format: beamer
---
```

Then render:

```bash
quarto render slides/<survey_key>/slides.qmd --to beamer
```

## Option 2: Native Beamer

Add:

```text
slides/<survey_key>/main.tex
scripts/build-slides.ps1
```

Use this when you want full LaTeX control or already have a Beamer template.

## Setup Notes

- Install a LaTeX distribution such as TinyTeX, MiKTeX, or TeX Live.
- Verify `latexmk` is available if your build script uses it.
- Keep generated PDFs and LaTeX build artifacts ignored by git.

## Codex Skill Tip

If you use LaTeX often, add a compile skill that tells Codex:

- which command builds the deck;
- where the final PDF should appear;
- where generated tables and figures live;
- how to inspect logs without editing raw data.
