# Protocolo — dataset pig fixo (train/val Kaggle)

Substitui os splits customizados S1–S3. Partição **única** já consolidada no repositório.

## Dados

| Partição | Caminho | Imagens (aprox.) |
| --- | --- | --- |
| Treino | `pig/train/images` | 929 |
| Validação | `pig/val/images` | 136 |
| Total | — | 1065 |

YAML: `experiments/data/yaml/pig_dataset.yaml` (gerado por `ensure_pig_dataset.py`).

## Experimentos

| ID | Modelo | Pesos iniciais | Framework | Venv | Ação |
| --- | --- | --- | --- | --- | --- |
| **E01** | YOLOv5s autoral | `yolov5s.pt` | YOLOv5 | `venv_yolo_5` | Treinar + validar |
| **E02** | YOLOv8s autoral | `yolov8s.pt` | Ultralytics | `venv_yolo_ultralytics` | Treinar + validar |
| **REF** | Terceiros | `pig/best.pt` | YOLOv5 | `venv_yolo_5` | Apenas validar |

## Métricas (val, `conf=0.25`)

Precision, Recall, mAP@0.50, mAP@0.50:0.95, F1, TP/FP/FN por imagem, tempos de inferência.

## Hipóteses

| ID | Hipótese |
| --- | --- |
| **H1** | E01 ≥ REF em mAP@0,50 e/ou Recall no mesmo `pig/val` |
| **H2a** | E02 ≥ E01 em mAP@0,50 e/ou mAP@0,50:0,95 no mesmo `pig/val` |

## Leitura das métricas (baseline E01 vs REF)

- **mAP@0.50 ~0,99** — saturado; diferenças pequenas são ruído.
- **mAP@0.50:0.95 ~0,83** — eixo mais informativo para caixas.
- **Recall** — maior diferença entre E01 e REF (~0,75 pp).

Ver [analise_desempenho_baseline.md](analise_desempenho_baseline.md).

## Comandos — YOLOv5 (E01 + REF)

```powershell
.\venv_yolo_5\Scripts\Activate.ps1
python experiments/shared/scripts/ensure_pig_dataset.py
python experiments/YOLO_V5/scripts/treinar.py E01
python experiments/YOLO_V5/scripts/validar.py E01
python experiments/YOLO_V5/scripts/validar.py REF
python experiments/shared/scripts/comparar.py
```

Ou: `.\experiments\YOLO_V5\run_pig_baseline.ps1`

## Comandos — YOLOv8 (E02)

```powershell
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
.\experiments\YOLO_V8\run_yolov8_pig.ps1
```

## Saídas

- `experiments/YOLO_V5/outputs/E01_yolov5s_pig/`
- `experiments/YOLO_V8/outputs/E02_yolov8s_pig/`
- `experiments/YOLO_V5/outputs/REF_best_pt_pig/`
- `experiments/shared/outputs/comparacao_pig_baseline.md`

## Fase futura

E03 YOLO11s, E04 YOLO11-R — mesmo `pig_dataset.yaml` e `venv_yolo_ultralytics` — planos 03–04.
