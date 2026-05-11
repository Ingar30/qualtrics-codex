# Setup Troubleshooting

The preferred setup is a local virtual environment with all requirements installed:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

On Windows, you can also run:

```powershell
.\scripts\setup.ps1
```

If virtual environment creation fails during `ensurepip`, Python may leave a partial `.venv/` directory. Remove the partial directory only after checking that it is the repo-local `.venv`, then either repair/reinstall Python or use the user-install fallback:

```powershell
Remove-Item -Recurse -Force .venv
.\scripts\setup.ps1 -User
```

The fallback installs packages such as `requests`, `pandas`, `matplotlib`, and `pytest` with `--user`. It is useful for getting started, but it is less reproducible than a working `.venv`.

If pytest cannot create temporary/cache directories in a restricted shell, use the helper that keeps those paths under `build/`:

```powershell
.\scripts\run_tests.ps1
```

## Missing Requests Or Pytest

If `scripts/qualtrics_workflow.py` says `requests` is missing, or `python -m pytest` says pytest is missing, install the repository requirements:

```powershell
python -m pip install -r requirements.txt
```

If you are not using an activated virtual environment:

```powershell
py -3 -m pip install --user -r requirements.txt
```

## Stata Not Found

The analysis wrapper tries Stata first and falls back to Python. If Stata is installed but not discoverable, set `STATA_EXE` explicitly:

```powershell
$env:STATA_EXE = "C:\Program Files\Stata19\StataMP-64.exe"
python scripts/run_analysis.py --survey-key repo_smoke_test --input build/fixtures/repo_smoke_test_responses.csv
```

To persist this for the repo, put the `STATA_EXE` line in `$HOME\.secrets\qualtrics.env.ps1` or your PowerShell profile.

The Python fallback is expected to work without Stata.

## Qualtrics Credentials Not Loaded

Synthetic tests do not need Qualtrics credentials. Live commands such as `check-auth`, `create-survey`, `get-link`, `submit-synthetic-responses`, and `export-responses` need local environment variables:

```powershell
. $HOME\.secrets\qualtrics.env.ps1
```

Check presence without printing values:

```powershell
if ($env:QUALTRICS_DATACENTER -and $env:QUALTRICS_API_TOKEN) { "Qualtrics env vars are set" }
```

## Qualtrics CSV Metadata Rows

Qualtrics CSV exports often include two metadata rows after the header. Real response IDs usually start with `R_`. Analysis scripts in this repo filter those rows when a `ResponseId` column is present.

When creating new analysis code, keep the same rule:

```text
keep rows where ResponseId starts with R_
```

## Draft Surveys And API Responses

Do not assume a draft or inactive survey means no data can be added through the API. Treat API-created test responses as live API mutations and ask explicitly before submitting them.

## Reusable Links And Metadata

`get-link` writes the reusable Qualtrics link to ignored metadata under `data/<survey_key>/metadata/`. It does not print the link unless you pass `--show-private-link`. Do not commit, paste, or publish reusable links or metadata by default.
