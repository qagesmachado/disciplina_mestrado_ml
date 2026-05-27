# Plano 02 — YOLOv8s: treino autoral padrão (pig fixo)

Detector **YOLOv8s** com pipeline **default** Ultralytics, no **mesmo** dataset que E01/REF (`pig/train` + `pig/val`).

**Matriz atual:** apenas **E02** — ver [protocolo_pig_fixo.md](protocolo_pig_fixo.md).  
Splits S1–S3 (E07/E08) ficam como **legado** em [protocolo_splits_e_experimentos.md](protocolo_splits_e_experimentos.md) (obsoleto).

---

## 1. Objetivo e hipótese

**Objetivo:** treinar YOLOv8s no domínio de leitões com augmentação padrão Ultralytics, comparável a E01 (YOLOv5s) e REF.

**Hipótese (H2a):** no mesmo `pig/val`, E02 apresenta mAP@0,50 e/ou mAP@0,50:0,95 **≥** E01, com mesmas épocas e `imgsz`.

---

## 2. Ambiente isolado (não impactar YOLOv5)

| Item | YOLOv5 (E01/REF) | YOLOv8 (E02) |
| --- | --- | --- |
| Venv | `venv_yolo_5` | `venv_yolo_ultralytics` |
| Requirements | `requirements-yolov5.txt` | `requirements-ultralytics.txt` |
| Treino | `YOLO_V5/scripts/treinar.py` | `YOLO_V8/scripts/treinar.py` |
| Validação | `YOLO_V5/scripts/validar.py` | `YOLO_V8/scripts/validar.py` |

**Não** instalar `ultralytics` no `venv_yolo_5` nem `yolov5` no `venv_yolo_ultralytics`.

**Setup (uma vez):**

```powershell
.\experiments\YOLO_V8\setup_venv_ultralytics.ps1
```

**Verificação:**

```powershell
.\venv_yolo_ultralytics\Scripts\python.exe -c "from ultralytics import YOLO; YOLO('yolov8s.pt'); print('OK')"
```

---

## 3. Dados

| Experimento | YAML | Train / Val |
| --- | --- | --- |
| E02 | `experiments/data/yaml/pig_dataset.yaml` | 929 / 136 |

Gerar YAML: `python experiments/shared/scripts/ensure_pig_dataset.py`

---

## 4. Configuração de treino

| Parâmetro | Valor | Fonte |
| --- | --- | --- |
| `model` | `yolov8s.pt` | [YOLO_V8/config/experiments.yaml](../experiments/YOLO_V8/config/experiments.yaml) |
| `imgsz` | 640 | defaults |
| `epochs` | 100 | defaults |
| `batch` | 16 (8 CPU) | defaults / CLI |
| `patience` | 20 | defaults |
| `seed` | 42 | defaults |
| Augmentação | **default Ultralytics** | registrar versão no `experiment_log.txt` |
| `project` | `experiments/YOLO_V8/outputs` | |
| `name` | `E02_yolov8s_pig` | |

---

## 5. Comandos

### Fluxo completo

```powershell
.\experiments\YOLO_V8\run_yolov8_pig.ps1
```

### Passo a passo

```powershell
.\venv_yolo_ultralytics\Scripts\Activate.ps1
python experiments/shared/scripts/ensure_pig_dataset.py
python experiments/YOLO_V8/scripts/treinar.py E02
python experiments/YOLO_V8/scripts/validar.py E02
.\venv_yolo_5\Scripts\python.exe experiments/shared/scripts/comparar.py
```

Teste rápido (CPU): `treinar_ultralytics.py E02 --epochs 2 --batch 4`

### Checkpoint

```
experiments/YOLO_V8/outputs/E02_yolov8s_pig/weights/best.pt
```

---

## 6. Validação

Mesmas métricas que E01: Precision, Recall, mAP@0,50, mAP@0,50:0,95, F1, TP/FP/FN, tempos.

Saídas: `experiments/YOLO_V8/outputs/E02_yolov8s_pig/val/metrics_summary.csv`

`conf=0,25` (padrão do protocolo).

---

## 7. Comparação

| Par | Objetivo |
| --- | --- |
| E02 vs E01 | **H2a** — YOLOv8 vs YOLOv5 |
| E02 vs REF | Autoral vs terceiros |
| E01 vs REF | **H1** (já documentada) |

Artefato: `experiments/shared/outputs/comparacao_pig_baseline.md` (inclui E02 quando validado).

---

## 8. Critérios de sucesso

- Treino estável; versão `ultralytics` no log
- H2a avaliada com métricas no mesmo `pig/val`
- Linha E02 em [templates/tabela_resultados_s1.csv](templates/tabela_resultados_s1.csv)
- **venv_yolo_5** intacto para E01/REF

---

## 9. Checklist pós-treino

- [ ] `setup_venv_ultralytics.ps1` executado
- [ ] E02 treinado e validado
- [ ] `comparar.py` com E01 + E02 + REF
- [ ] Discussão H2a no artigo

---

## Referências

- [Plano 01 — YOLOv5s](plano_01_yolov5_treino_proprio.md)
- [Protocolo pig fixo](protocolo_pig_fixo.md)
- [experiments/README.md](../experiments/README.md)
