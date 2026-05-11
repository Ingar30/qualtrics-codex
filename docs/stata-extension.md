# Stata First, Python Fallback

The default starter workflow assumes many economists already have Stata installed. The repository therefore prefers Stata for survey analysis, but it does not require Stata for the first run.

## One Analysis Command

Run:

```bash
python scripts/run_analysis.py --survey-key <survey_key>
```

The analysis script:

- looks for `code/<survey_key>/analysis/run.do`;
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

Keep Stata files survey-specific and readable. Add comments before each major block so the workflow remains teachable. Keep the Python file as the guaranteed fallback.

## Environment

Set `STATA_EXE` to your Stata executable if it is not on PATH.

Windows PowerShell example:

```powershell
$env:STATA_EXE = "C:\Stata19\StataSE-64.exe"
```

macOS/Linux users can set `STATA_EXE` to the local `stata-mp`, `stata-se`, or `stata` batch executable if it is not already on PATH.

## Data Flow

1. Export CSV from Qualtrics:

   ```bash
   python scripts/qualtrics_workflow.py export-responses --survey-key <survey_key> --format csv
   ```

2. `scripts/run_analysis.py` passes the newest raw CSV to Stata when Stata is available.
3. Stata or Python writes `data/<survey_key>/processed/clean.csv`.
4. Stata or Python writes slide inputs under `slides/<survey_key>/inputs/`.
5. Figure PDFs are for Beamer; figure PNGs are for the Python HTML fallback.
6. `scripts/build_slides.py` builds Beamer slides from those inputs or falls back to `slides/<survey_key>/slides.md`.

## Codex Skill Tip

If you rely on Stata regularly, add a repo-local skill that tells Codex:

- where Stata lives on your machine;
- how to run batch `.do` files;
- where raw, processed, metadata, and slide-input files belong;
- that figure PDFs and PNGs should both be exported;
- that raw exports must not be edited after download.
