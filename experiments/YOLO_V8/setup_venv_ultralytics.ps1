# Cria venv_yolo_ultralytics na raiz do repo (E02 YOLOv8 + E03 YOLO11 — mesmo pacote ultralytics).
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

& $PythonExe -c "from ultralytics import YOLO; import ultralytics; YOLO('yolov8s.pt'); YOLO('yolo11s.pt'); print('OK ultralytics', ultralytics.__version__, '| yolov8s + yolo11s')"

$cudaOk = & $PythonExe -c "import torch; print(torch.cuda.is_available())"
if ($cudaOk -ne "True") {
    Write-Host "`n[AVISO] PyTorch instalado sem CUDA (comum no pip padrao)." -ForegroundColor Yellow
    Write-Host "  Para treinar na GPU: .\experiments\YOLO_V8\setup_pytorch_gpu.ps1" -ForegroundColor Yellow
    Write-Host "  Depois confira: .\experiments\YOLO_V8\verify_ultralytics_gpu.ps1" -ForegroundColor Yellow
} else {
    $gpuName = & $PythonExe -c "import torch; print(torch.cuda.get_device_name(0))"
    Write-Host "`n[OK] CUDA detectada: $gpuName" -ForegroundColor Green
}

Write-Host "`nPronto (venv compartilhado E02 + E03):" -ForegroundColor Green
Write-Host "  .\experiments\YOLO_V8\run_yolov8_pig.ps1" -ForegroundColor Green
Write-Host "  .\experiments\YOLO_V11\run_yolov11_pig.ps1" -ForegroundColor Green
