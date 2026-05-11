param(
    [switch]$User
)

$ErrorActionPreference = "Stop"

function Invoke-RepoPython {
    param([string[]]$Arguments)

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 @Arguments
        return
    }

    & python @Arguments
}

if ($User) {
    Invoke-RepoPython @("-m", "pip", "install", "--user", "-r", "requirements.txt")
    Write-Host "Installed requirements with --user. Run repo commands with the same Python."
    exit 0
}

if (Test-Path ".venv") {
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        throw "Found a partial .venv without .venv\Scripts\python.exe. Remove .venv, then rerun this script. If venv creation still fails, try: .\scripts\setup.ps1 -User"
    }
} else {
    Invoke-RepoPython @("-m", "venv", ".venv")
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "Environment ready. Activate with: .\.venv\Scripts\Activate.ps1"
