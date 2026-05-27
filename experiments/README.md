# Experimentos — estrutura por versão YOLO

```
experiments/
  data/                 # Dataset compartilhado (pig_dataset.yaml)
  shared/
    scripts/            # ensure_pig_dataset, comparar, métricas, paths
    outputs/            # Comparação E01+E02+REF (comparacao_pig_baseline.md)
  YOLO_V5/              # E01 + REF — venv_yolo_5
    config/
    scripts/
    outputs/
    run_pig_baseline.ps1
  YOLO_V8/              # E02 — venv_yolo_ultralytics
    config/
    scripts/
    outputs/
    run_yolov8_pig.ps1
    setup_venv_ultralytics.ps1
```

## Ambientes

| Venv | Pasta | Requirements |
| --- | --- | --- |
| `venv_yolo_5` | `YOLO_V5/` | `requirements-yolov5.txt` |
| `venv_yolo_ultralytics` | `YOLO_V8/` | `requirements-ultralytics.txt` |

## Fluxos

```powershell
# YOLOv5 (E01 + REF)
.\experiments\YOLO_V5\run_pig_baseline.ps1

# YOLOv8 (E02) — após setup do venv
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
.\experiments\YOLO_V8\setup_pytorch_gpu.ps1   # necessário no Windows: pip traz torch CPU-only
.\experiments\YOLO_V8\run_yolov8_pig.ps1
```

No início do treino deve aparecer `[INFO] GPU CUDA detectada — usando device 0`. Se aparecer CPU, rode `setup_pytorch_gpu.ps1` e treine de novo.

Documentação TCD: [entrega_parte_b_c/](../entrega_parte_b_c/)
