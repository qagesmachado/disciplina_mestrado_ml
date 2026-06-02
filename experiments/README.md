# Experimentos — estrutura por versão YOLO

```
experiments/
  data/                 # Dataset compartilhado (pig_dataset.yaml)
  shared/
    scripts/            # ensure_pig_dataset, comparar, métricas, paths
    outputs/            # Comparação E01+E02+E03 (comparacao_pig_baseline.md)
  YOLO_V5/              # E01 — venv_yolo_5
    config/
    scripts/
    outputs/
    run_pig_baseline_yolov5.ps1
  YOLO_V8/              # E02 — venv_yolo_ultralytics
    config/
    scripts/
    outputs/
    run_yolov8_pig.ps1
    setup_venv_ultralytics.ps1
  YOLO_V11/             # E03 — venv_yolo_ultralytics (mesmo venv)
    config/
    scripts/
    outputs/
    run_yolov11_pig.ps1
```

## Ambientes

| Venv | Pasta | Requirements |
| --- | --- | --- |
| `venv_yolo_5` | `YOLO_V5/` | `requirements-yolov5.txt` |
| `venv_yolo_ultralytics` | `YOLO_V8/` (E02), `YOLO_V11/` (E03) | `requirements-ultralytics.txt` |

## Fluxos

```powershell
# YOLOv5 (E01)
.\experiments\YOLO_V5\run_pig_baseline_yolov5.ps1

# YOLOv8 (E02) — após setup do venv
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
.\experiments\YOLO_V8\setup_pytorch_gpu.ps1   # necessário no Windows: pip traz torch CPU-only
.\experiments\YOLO_V8\run_yolov8_pig.ps1

# YOLO11 (E03) — mesmo venv do E02
.\experiments\YOLO_V11\run_yolov11_pig.ps1
```

No início do treino deve aparecer `[INFO] GPU CUDA detectada — usando device 0`. Se aparecer CPU, rode `setup_pytorch_gpu.ps1` e treine de novo.

**Um venv, dois detectores:** `venv_yolo_ultralytics` + `requirements-ultralytics.txt` servem E02 (`yolov8s.pt`) e E03 (`yolo11s.pt`). Não é necessário venv nem requirements separados por versão YOLO — só o arquivo de pesos muda.

Verificação rápida de GPU + modelos:

```powershell
.\experiments\YOLO_V8\verify_ultralytics_gpu.ps1
```

Documentação TCD: [entrega_parte_2/](../entrega_parte_2/)
