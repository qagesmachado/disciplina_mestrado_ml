# Verifica CUDA + carregamento yolov8s.pt e yolo11s.pt no venv_yolo_ultralytics.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

$PythonExe = ".\venv_yolo_ultralytics\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "Crie o venv: .\experiments\YOLO_V8\setup_venv_ultralytics.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "=== nvidia-smi ===" -ForegroundColor Cyan
nvidia-smi | Select-Object -First 12

Write-Host "`n=== PyTorch / Ultralytics ===" -ForegroundColor Cyan
& $PythonExe -c @"
import torch
import ultralytics
print('ultralytics', ultralytics.__version__)
print('torch', torch.__version__)
print('cuda available', torch.cuda.is_available())
if torch.cuda.is_available():
    print('gpu', torch.cuda.get_device_name(0))
"@

Write-Host "`n=== Smoke test GPU (yolov8s + yolo11s) ===" -ForegroundColor Cyan
& $PythonExe -c @"
from ultralytics import YOLO
import torch

if not torch.cuda.is_available():
    raise SystemExit('CUDA indisponivel. Rode: .\\experiments\\YOLO_V8\\setup_pytorch_gpu.ps1')

for weights in ('yolov8s.pt', 'yolo11s.pt'):
    model = YOLO(weights)
    results = model.predict(source='https://ultralytics.com/images/bus.jpg', device=0, verbose=False)
    print(f'OK {weights} on GPU, boxes={len(results[0].boxes)}')
"@

Write-Host "`nPronto: E02 e E03 podem usar o mesmo venv_yolo_ultralytics." -ForegroundColor Green
