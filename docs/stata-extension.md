# Stata First, Python Fallback

The default starter workflow assumes many economists already have Stata installed. The repository therefore prefers Stata for survey analysis, but it does not require Stata for the first run.

## One Analysis Command

Run:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
```

The analysis script:

- first looks for the lab-style pair `code/<survey_key>/cleaning/run.do` and `code/<survey_key>/figures/run.do` with `scripts/stata/survey_pipeline.do`;
- otherwise looks for `code/<survey_key>/analysis/run.do`;
- tries to run it with `STATA_EXE`, Stata on PATH, or common Stata install locations;
- writes Stata logs under `data/<survey_key>/metadata/`;
- falls back to `code/<survey_key>/analysis/run.py` if Stata is missing or fails.

To force one path:

```bash
python scripts/run_analysis.py --survey-key <survey_key> --mode stata
python scripts/run_analysis.py --survey-key <survey_key> --mode python
```

Use `--mode stata` when you want a nonzero exit code if Stata fails.

## Expected Source Files

```text
code/<survey_key>/analysis/run.do
code/<survey_key>/analysis/run.py
```

For the lab-style SPSS/Stata path, use:

```text
code/<survey_key>/cleaning/run.do
code/<survey_key>/figures/run.do
code/<survey_key>/analysis/run.py
```

Keep Stata files survey-specific and readable. Add comments before each major block so the workflow remains teachable. Keep the Python file as the guaranteed fallback.

## Environment

Set `STATA_EXE` to your Stata executable if it is not on PATH.

Windows PowerShell example:

```powershell
$env:STATA_EXE = "C:\Program Files\Stata19\StataMP-64.exe"
```

macOS/Linux users can set `STATA_EXE` to the local `stata-mp`, `stata-se`, or `stata` batch executable if it is not already on PATH.

## Data Flow

1. Export SPSS/SAV from Qualtrics for the Stata path. Use CSV for Python workflows.

   ```bash
   python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format spss
   ```

2. Stata imports the newest raw `.sav` with `import spss`.
3. Stata writes `data/<survey_key>/processed/clean.dta` and any CSV/table outputs needed by the slides.
4. Stata writes slide inputs under `slides/<survey_key>/inputs/`.
5. Figure PDFs are for Beamer; figure PNGs are for the Python HTML fallback.
6. `scripts/build_slides.py` builds Beamer slides from those inputs or falls back to `slides/<survey_key>/slides.md`.

## Codex Skill Tip

If you rely on Stata regularly, add a repo-local skill that tells Codex:

- where Stata lives on your machine;
- how to run batch `.do` files;
- where raw, processed, metadata, and slide-input files belong;
- that figure PDFs and PNGs should both be exported;
- that raw exports must not be edited after download.
