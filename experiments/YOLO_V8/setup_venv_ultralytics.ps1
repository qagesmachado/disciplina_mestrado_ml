# Cria venv_yolo_ultralytics na raiz do repo
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

$VenvDir = "venv_yolo_ultralytics"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"
$ReqFile = "requirements-ultralytics.txt"

if (-not (Test-Path $VenvDir)) {
    Write-Host "Criando $VenvDir ..." -ForegroundColor Cyan
    python -m venv $VenvDir
}

& $PythonExe -m pip install -U pip
& $PythonExe -m pip install -r $ReqFile

& $PythonExe -c "from ultralytics import YOLO; import ultralytics; YOLO('yolov8s.pt'); print('OK', ultralytics.__version__)"

$cudaOk = & $PythonExe -c "import torch; print(torch.cuda.is_available())"
if ($cudaOk -ne "True") {
    Write-Host "`n[AVISO] PyTorch instalado sem CUDA (comum no pip padrao)." -ForegroundColor Yellow
    Write-Host "  Para treinar na GPU: .\experiments\YOLO_V8\setup_pytorch_gpu.ps1" -ForegroundColor Yellow
}

Write-Host "`nPronto. Rode: .\experiments\YOLO_V8\run_yolov8_pig.ps1" -ForegroundColor Green
