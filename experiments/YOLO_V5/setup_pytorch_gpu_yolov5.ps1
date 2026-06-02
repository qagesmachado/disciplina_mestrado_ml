# Reinstala PyTorch com CUDA no venv_yolo_5 (Windows + NVIDIA).
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

if (-not (Test-Path ".\venv_yolo_5\Scripts\Activate.ps1")) {
    Write-Host "Crie o venv antes: python -m venv venv_yolo_5" -ForegroundColor Red
    exit 1
}

Write-Host "Verificando GPU (nvidia-smi)..." -ForegroundColor Cyan
nvidia-smi | Select-Object -First 12

.\venv_yolo_5\Scripts\Activate.ps1

Write-Host "`nPyTorch atual:" -ForegroundColor Cyan
python -c "import torch; print(torch.__version__, 'cuda=', torch.cuda.is_available())"

Write-Host "`nRemovendo build CPU-only..." -ForegroundColor Cyan
pip uninstall -y torch torchvision torchaudio *> $null

$CudaIndex = "https://download.pytorch.org/whl/cu130"
pip install torch torchvision --index-url $CudaIndex

Write-Host "`nVerificacao:" -ForegroundColor Green
python -c "import torch; print('cuda', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
Write-Host "  python experiments/YOLO_V5/scripts/treinar_yolov5.py E01 --epochs 2 --device 0" -ForegroundColor Green
