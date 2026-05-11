# LaTeX, Beamer, And PDF Extension

The default starter workflow uses native HTML slides because they render without Quarto, R, Node, or a TeX installation. Use this extension if you prefer Beamer or PDF slides.

## Option 1: Export Native HTML Slides To PDF

Use the built-in renderer's optional browser export:

```bash
python scripts/render_slides.py --survey-key <survey_key> --pdf
```

This uses Chrome, Edge, or Chromium when one is installed. If browser discovery fails, open `build/slides/<survey_key>/slides.html` and use Print to PDF manually.

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
