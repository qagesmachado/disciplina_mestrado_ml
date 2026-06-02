# YOLO_V5 — E01

Treino autoral YOLOv5s no dataset pig fixo. Venv: `venv_yolo_5`.

| Script | Função |
| --- | --- |
| `run_pig_baseline_yolov5.ps1` | Fluxo completo: dataset → treino → validar → comparar |
| `scripts/treinar_yolov5.py` | Treina E01 |
| `scripts/validar_yolov5.py` | Valida E01 |
| `../shared/scripts/comparar.py` | Compara E01–E03 (se existirem) |

**Config:** `config/experiments_yolov5.yaml` — campo `weights_init` (`yolov5n.pt` ou `yolov5s.pt`).

**Saída:** `experiments/YOLO_V5/outputs/E01_yolov5s_pig/`
