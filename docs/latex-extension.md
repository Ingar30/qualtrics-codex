# LaTeX, Beamer, And PDF Extension

The default starter workflow uses native HTML slides because they render without Quarto, R, Node, or a TeX installation. Use this extension if you prefer Beamer or PDF slides.

## Option 1: Print HTML Slides To PDF

Open `build/slides/<survey_key>/slides.html` in a browser and print to PDF. This keeps the base workflow dependency-light.

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
