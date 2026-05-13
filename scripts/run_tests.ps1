param()

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

$TempRoot = Join-Path $ProjectRoot "build\pytest-tmp-$PID"
$CacheRoot = Join-Path $ProjectRoot "build\pytest-cache-$PID"

New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
New-Item -ItemType Directory -Force -Path $CacheRoot | Out-Null

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m pytest --basetemp $TempRoot -o "cache_dir=$CacheRoot"
if ($LASTEXITCODE -ne 0) {
    throw "pytest failed with exit code $LASTEXITCODE."
}
