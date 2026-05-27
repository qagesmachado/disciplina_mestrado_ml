# YOLO_V5 — E01 + REF

**Venv:** `venv_yolo_5` (raiz do repo)

```powershell
.\experiments\YOLO_V5\run_pig_baseline.ps1
```

| Script | Função |
| --- | --- |
| `scripts/treinar.py` | Treina E01 |
| `scripts/validar.py` | Valida E01 ou REF |
| `../shared/scripts/comparar.py` | Compara com E02 (se existir) |

**Saídas:** `experiments/YOLO_V5/outputs/E01_yolov5s_pig/`, `REF_best_pt_pig/`
