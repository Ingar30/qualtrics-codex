# Beamer First, Python Fallback

The default starter workflow assumes many economists already have LaTeX/Beamer installed. The repository therefore prefers Beamer, but it does not require Beamer for the first run.

## One Build Command

Run:

```bash
python scripts/build_slides.py --survey-key <survey_key>
```

The build script:

- looks for `slides/<survey_key>/main.tex`;
- tries to compile it with `latexmk`, `xelatex`, `pdflatex`, `lualatex`, or `tectonic`;
- writes a successful Beamer PDF to `build/slides/<survey_key>/slides.pdf`;
- falls back to `slides/<survey_key>/slides.md` through the native Python renderer if LaTeX is missing or fails.

The fallback HTML appears at:

```text
build/slides/<survey_key>/slides.html
```

If Chrome, Edge, or Chromium is already installed, the fallback also tries to create:

```text
build/slides/<survey_key>/slides.pdf
```

## Expected Source Files

Keep both decks in the survey slide folder:

```text
slides/<survey_key>/main.tex
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/
```

The Beamer deck should prefer vector figure PDFs from `inputs/` instead of raster PNGs. The Markdown deck is the fallback path and should use the PNGs with the same base filenames.

## Force One Path

```bash
python scripts/build_slides.py --survey-key <survey_key> --mode beamer
python scripts/build_slides.py --survey-key <survey_key> --mode python
```

Use `--mode beamer` when you want a nonzero exit code if LaTeX fails. Use `--mode python` when you want the no-install fallback directly.

## Setup Notes

- Install a LaTeX distribution such as TinyTeX, MiKTeX, or TeX Live.
- `latexmk` is preferred, but the build script also checks direct engines.
- On macOS, use MacTeX or TinyTeX; Homebrew can install MacTeX with `brew install --cask mactex`.
- On Windows, MiKTeX is usually the lowest-friction choice.
- Keep generated PDFs and LaTeX build artifacts ignored by git.

## Codex Skill Tip

If you use LaTeX often, add a compile skill that tells Codex:

- that `python scripts/build_slides.py --survey-key <survey_key>` is the default build command;
- where the final PDF should appear;
- where generated tables and figures live;
- how to inspect logs without editing raw data.
