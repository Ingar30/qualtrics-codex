param()

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

New-Item -ItemType Directory -Force -Path "build\pytest-tmp" | Out-Null
New-Item -ItemType Directory -Force -Path "build\pytest_cache" | Out-Null

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m pytest --basetemp "build\pytest-tmp"
if ($LASTEXITCODE -ne 0) {
    throw "pytest failed with exit code $LASTEXITCODE."
}
