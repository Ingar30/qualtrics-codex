param(
    [string]$SurveyKey = "repo_smoke_test",
    [string]$LatexEngine,
    [switch]$PythonFallbackOnly
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

$Mode = if ($PythonFallbackOnly) { "python" } else { "auto" }
$Args = @("scripts\build_slides.py", "--survey-key", $SurveyKey, "--mode", $Mode)
if ($LatexEngine) {
    $Args += @("--latex-engine", $LatexEngine)
}

& $Python @Args
if ($LASTEXITCODE -ne 0) {
    throw "Slide build failed with exit code $LASTEXITCODE."
}
