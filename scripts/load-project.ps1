param(
    [switch]$RequireQualtrics
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . ".\.venv\Scripts\Activate.ps1"
    Write-Host "Python virtual environment activated."
}
else {
    Write-Warning "Python virtual environment not found at .\.venv\Scripts\Activate.ps1. Run .\scripts\setup.ps1 first."
}

$SecretsFile = Join-Path $HOME ".secrets\qualtrics.env.ps1"
if (Test-Path $SecretsFile) {
    . $SecretsFile
    Write-Host "Loaded local Qualtrics secrets file without printing secret values."
}
elseif ($RequireQualtrics) {
    throw "Qualtrics secrets file not found: $SecretsFile"
}
else {
    Write-Warning "Qualtrics secrets file not found. This is fine for local synthetic tests."
}

if ($RequireQualtrics) {
    if (-not $env:QUALTRICS_DATACENTER) {
        throw "QUALTRICS_DATACENTER is missing."
    }
    if (-not $env:QUALTRICS_API_TOKEN) {
        throw "QUALTRICS_API_TOKEN is missing."
    }
    Write-Host "Qualtrics credentials are present. Values were not printed."
}

if ($env:STATA_EXE) {
    if (Test-Path $env:STATA_EXE) {
        Write-Host "STATA_EXE is set and points to an existing file."
    }
    else {
        throw "STATA_EXE is set but the file does not exist. Update `$env:STATA_EXE in your local secrets file or shell."
    }
}
else {
    Write-Warning "STATA_EXE is not set. Python wrappers will try common Stata executable names and paths."
}
