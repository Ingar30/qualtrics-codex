param(
    [Parameter(Mandatory = $true)]
    [string]$SurveyKey,

    [string]$SurveyName,
    [string]$SurveyId,
    [ValidateSet("csv", "spss")]
    [string]$Format = "spss"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ProjectRoot

. ".\scripts\load-project.ps1" -RequireQualtrics

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

$ExportArgs = @("scripts\qualtrics_workflow.py", "export-responses", "--survey-key", $SurveyKey, "--format", $Format)
if ($SurveyId) {
    $ExportArgs += @("--survey-id", $SurveyId)
}
elseif ($SurveyName) {
    $ExportArgs += @("--survey-name", $SurveyName)
}

& $Python @ExportArgs
if ($LASTEXITCODE -ne 0) {
    throw "Qualtrics export failed with exit code $LASTEXITCODE."
}

& $Python "scripts\run_analysis.py" "--survey-key" $SurveyKey
if ($LASTEXITCODE -ne 0) {
    throw "Analysis failed with exit code $LASTEXITCODE."
}

& $Python "scripts\build_slides.py" "--survey-key" $SurveyKey
if ($LASTEXITCODE -ne 0) {
    throw "Slide build failed with exit code $LASTEXITCODE."
}

Write-Host "Pipeline complete."
Write-Host "Raw export: data\$SurveyKey\raw\"
Write-Host "Processed data: data\$SurveyKey\processed\"
Write-Host "Slide inputs: slides\$SurveyKey\inputs\"
Write-Host "Slides: build\slides\$SurveyKey\"
