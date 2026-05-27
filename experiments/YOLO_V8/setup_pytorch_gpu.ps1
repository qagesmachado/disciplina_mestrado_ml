# Reinstala PyTorch com CUDA no venv_yolo_ultralytics (Windows + NVIDIA).
# pip install -r requirements-ultralytics.txt costuma trazer torch CPU-only; este script corrige.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

$PythonExe = ".\venv_yolo_ultralytics\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "Crie o venv antes: .\experiments\YOLO_V8\setup_venv_ultralytics.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "Verificando GPU (nvidia-smi)..." -ForegroundColor Cyan
nvidia-smi | Select-Object -First 12

Write-Host "`nPyTorch atual:" -ForegroundColor Cyan
& $PythonExe -c "import torch; print(torch.__version__, 'cuda=', torch.cuda.is_available())"

Write-Host "`nRemovendo build CPU-only..." -ForegroundColor Cyan
& $PythonExe -m pip uninstall -y torch torchvision torchaudio *> $null

$CudaIndex = "https://download.pytorch.org/whl/cu130"
& $PythonExe -m pip install torch torchvision --index-url $CudaIndex

Write-Host "`nVerificacao:" -ForegroundColor Green
& $PythonExe -c "import torch; print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
Write-Host "  .\experiments\YOLO_V8\run_yolov8_pig.ps1" -ForegroundColor Green
Write-Host "  (ou treino curto: python experiments/YOLO_V8/scripts/treinar.py E02 --epochs 2 --device 0)" -ForegroundColor Green
