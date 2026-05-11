# Reproducibility Notes

The workflow has two public commands after a survey response export:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
python scripts/build_slides.py --survey-key <survey_key>
```

## Analysis Contract

`scripts/run_analysis.py` tries Stata first and falls back to Python. Both paths should write the same files:

```text
data/<survey_key>/processed/clean.csv
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/<figure>.pdf
slides/<survey_key>/inputs/<figure>.png
```

Use figure PDFs in Beamer. Use figure PNGs in the Python HTML fallback.

## Slide Contract

`scripts/build_slides.py` tries Beamer first and falls back to Python. Beamer reads:

```text
slides/<survey_key>/main.tex
slides/<survey_key>/inputs/summary.tex
slides/<survey_key>/inputs/*.pdf
```

The Python fallback reads:

```text
slides/<survey_key>/slides.md
slides/<survey_key>/inputs/summary.md
slides/<survey_key>/inputs/*.png
```

## Force A Backend

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
python scripts/run_analysis.py --survey-key <survey_key> --mode python
python scripts/build_slides.py --survey-key <survey_key> --mode beamer
python scripts/build_slides.py --survey-key <survey_key> --mode python
```

Forced modes are useful for debugging. The default `auto` mode is for collaborators who may not have the same local tools installed.
