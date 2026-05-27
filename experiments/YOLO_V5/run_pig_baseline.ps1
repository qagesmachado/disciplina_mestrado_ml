# Fluxo YOLOv5: dataset → treino E01 → validar E01+REF → comparar
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

$PythonExe = ".\venv_yolo_5\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "Crie o venv: python -m venv venv_yolo_5" -ForegroundColor Red
    exit 1
}

function Step($Label, [string[]]$Cmd) {
    Write-Host "`n=== $Label ===" -ForegroundColor Cyan
    & $PythonExe @Cmd
    if ($LASTEXITCODE -ne 0) { throw "Falhou (exit $LASTEXITCODE)" }
}

Step "1/5 Dataset" @("experiments/shared/scripts/ensure_pig_dataset.py")
Step "2/5 Treino E01" @("experiments/YOLO_V5/scripts/treinar.py", "E01")
Step "3/5 Validar E01" @("experiments/YOLO_V5/scripts/validar.py", "E01")
Step "4/5 Validar REF" @("experiments/YOLO_V5/scripts/validar.py", "REF")
Step "5/5 Comparar" @("experiments/shared/scripts/comparar.py")

Write-Host "`nOK: experiments/shared/outputs/comparacao_pig_baseline.md" -ForegroundColor Green
