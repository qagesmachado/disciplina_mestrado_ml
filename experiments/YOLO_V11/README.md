# YOLO_V11 — E03 (YOLO11s autoral)

Treino e validação no dataset pig fixo (`pig/train` + `pig/val`).

## Pré-requisitos

Usa o mesmo venv do E02:

```powershell
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
.\experiments\YOLO_V8\setup_pytorch_gpu.ps1   # se treinar na GPU (Windows)
```

Verificar suporte YOLO11:

```powershell
.\venv_yolo_ultralytics\Scripts\python.exe -c "from ultralytics import YOLO; YOLO('yolo11s.pt'); print('OK')"
```

## Fluxo completo

```powershell
.\experiments\YOLO_V11\run_yolov11_pig.ps1
```

## Comandos individuais

```powershell
python experiments/shared/scripts/ensure_pig_dataset.py
python experiments/YOLO_V11/scripts/treinar.py E03
python experiments/YOLO_V11/scripts/validar.py E03
python experiments/shared/scripts/comparar.py
```

## Saídas

- `outputs/E03_yolo11s_pig/weights/best.pt`
- `outputs/E03_yolo11s_pig/val/metrics_summary.csv`
- Comparação: `experiments/shared/outputs/comparacao_pig_baseline.md`
