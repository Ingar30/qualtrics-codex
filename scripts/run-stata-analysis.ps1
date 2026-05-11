param(
    [Parameter(Mandatory = $true)]
    [string]$SurveyKey,

    [string]$Input,

    [string]$StataExe
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

$Args = @("scripts\run_analysis.py", "--survey-key", $SurveyKey, "--mode", "stata")
if ($Input) {
    $Args += @("--input", $Input)
}
if ($StataExe) {
    $Args += @("--stata-exe", $StataExe)
}

& $Python @Args
if ($LASTEXITCODE -ne 0) {
    throw "Stata analysis failed with exit code $LASTEXITCODE."
}
