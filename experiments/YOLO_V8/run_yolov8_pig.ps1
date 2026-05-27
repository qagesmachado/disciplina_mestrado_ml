# Fluxo YOLOv8 E02 — venv_yolo_ultralytics
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

$PythonExe = ".\venv_yolo_ultralytics\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "Crie o venv: .\experiments\YOLO_V8\setup_venv_ultralytics.ps1" -ForegroundColor Red
    exit 1
}

function Step($Label, [string[]]$Cmd) {
    Write-Host "`n=== $Label ===" -ForegroundColor Cyan
    & $PythonExe @Cmd
    if ($LASTEXITCODE -ne 0) { throw "Falhou (exit $LASTEXITCODE)" }
}

Step "1/4 Dataset" @("experiments/shared/scripts/ensure_pig_dataset.py")
Step "2/4 Treino E02" @("experiments/YOLO_V8/scripts/treinar.py", "E02")
Step "3/4 Validar E02" @("experiments/YOLO_V8/scripts/validar.py", "E02")

Write-Host "`n=== 4/4 Comparar ===" -ForegroundColor Cyan
$Py5 = ".\venv_yolo_5\Scripts\python.exe"
if (Test-Path $Py5) { & $Py5 experiments/shared/scripts/comparar.py }
else { & $PythonExe experiments/shared/scripts/comparar.py }
if ($LASTEXITCODE -ne 0) { throw "Falhou comparar" }

Write-Host "`nOK: experiments/shared/outputs/comparacao_pig_baseline.md" -ForegroundColor Green
