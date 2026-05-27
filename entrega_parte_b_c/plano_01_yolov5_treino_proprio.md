# Plano 01 — YOLOv5s: treino autoral do zero

Experimento de detecção com **YOLOv5s treinado pelo autor** no dataset de leitões. O checkpoint `pig/best.pt` é apenas **referência externa** (Etapa 1), nunca peso inicial.

**Matriz:** E01 no dataset **pig fixo** (train/val Kaggle) — ver [protocolo_pig_fixo.md](protocolo_pig_fixo.md).

---

## 1. Objetivo e hipótese

**Objetivo:** obter um detector YOLOv5s fine-tuned no domínio de leitões em cenas densas, reprodutível e comparável a YOLOv8s, YOLO11s e YOLO11-R.

**Hipótese (H1):** o modelo autoral E01 atinge desempenho **igual ou superior** ao `best.pt` de terceiros no **mesmo** `pig/val`, em mAP@0,50 e/ou Recall.

---

## 2. Pré-requisitos

| Item | Detalhe |
| --- | --- |
| Python | 3.10+ (recomendado; ver [README](../README.md)) |
| Ambiente | `venv_yolo_5` ativado |
| Pacotes | `pip install -r requirements.txt` (`yolov5==7.0.14`, torch, etc.) |
| GPU | Recomendada; CPU possível com batch menor |
| Dados | `experiments/data/yaml/pig_dataset.yaml` (`ensure_pig_dataset.py`) |
| Pesos iniciais | `yolov5s.pt` baixado automaticamente no primeiro treino (**não** usar `pig/best.pt`) |

**Verificação rápida:**

```powershell
python -c "import yolov5, torch; print('OK', torch.__version__)"
```

---

## 3. Dados

| Experimento | YAML | Train / Val |
| --- | --- | --- |
| E01 | `pig_dataset.yaml` | 929 train / 136 val |

**Antes do primeiro treino:** `python experiments/YOLO_V5/scripts/ensure_pig_dataset.py` — ver [experiments/README.md](../experiments/README.md).

---

## 4. Configuração de treino

| Parâmetro | Valor | Notas |
| --- | --- | --- |
| `model` / `--weights` | `yolov5s.pt` | COCO pretrained |
| `imgsz` | 640 | |
| `epochs` | 100 | |
| `batch` | 16 (GPU 8GB+) ou 8 | registrar valor usado |
| `patience` | 20 | |
| `seed` | 42 | |
| `workers` | 4 | ajustar SO |
| `device` | `0` ou `cpu` | |
| Augmentação | **default YOLOv5** (`hyp.scratch-low.yaml` ou padrão do pacote) | mosaic, mixup, HSV padrão |
| `project` | `experiments/YOLO_V5/outputs` | |
| `name` | `E01_yolov5s_pig` | |

**Não alterar** augmentação neste plano (contraste com YOLO11-R, Plano 04).

---

## 5. Comandos (pasta `experiments/`)

### 5.1 Fluxo E01 (Fase 1)

```powershell
cd c:\repositories\repositories-mestrado\disciplina_ml_privado
.\venv_yolo_5\Scripts\Activate.ps1

python experiments/YOLO_V5/scripts/ensure_pig_dataset.py
python experiments/YOLO_V5/scripts/treinar.py E01
python experiments/YOLO_V5/scripts/validar.py E01
python experiments/YOLO_V5/scripts/validar.py REF
python experiments/YOLO_V5/scripts/comparar.py
```

Atalho: `.\experiments\YOLO_V5\run_pig_baseline.ps1`

### 5.2 Localização do melhor checkpoint

```
experiments/YOLO_V5/outputs/E01_yolov5s_pig/weights/best.pt
```

---

## 6. Validação

Script: [experiments/YOLO_V5/scripts/validar.py](../experiments/YOLO_V5/scripts/validar.py)

| Argumento | E01 |
| --- | --- |
| `exp_id` | `E01` |
| `--weights` | (opcional) default: `experiments/YOLO_V5/outputs/E01_yolov5s_pig/weights/best.pt` |
| `conf_thres` | 0.25 |
| `imgsz` | 640 |

**Saídas:**

```
experiments/YOLO_V5/outputs/E01_yolov5s_pig/val/
  metrics_summary.csv
  val_report.html
  per_image_tp_fp_fn.csv
```

---

## 7. Saídas esperadas

| Artefato | Caminho |
| --- | --- |
| Pesos treinados | `experiments/YOLO_V5/outputs/E0X_yolov5s_*/weights/best.pt` |
| Log de treino | `experiments/YOLO_V5/outputs/E0X_*/results.csv` |
| Gráficos | `experiments/YOLO_V5/outputs/E0X_*/results.png` |
| Validação | `experiments/YOLO_V5/outputs/E0X_*/val/metrics_summary.csv` |
| Relatório HTML | `experiments/YOLO_V5/outputs/E0X_*/val/val_report.html` |

---

## 8. Comparação com outros modelos

| Momento | Comparação |
| --- | --- |
| Após E01 | REF (`pig/best.pt`) no **mesmo S1** — tabela lado a lado |
| Após Fase 1 completa | E01 vs E02 vs E03 vs E04 (val limpo) |
| Val degradado | E03 vs E04 (YOLO11 vs YOLO11-R) |
| Fase 2 | E05/E06 vs E01 — efeito do split |

**Texto para artigo:** deixar claro que REF é modelo de terceiros citado na Etapa 1; E01 é contribuição experimental autoral.

---

## 9. Critérios de sucesso

| Critério | Meta qualitativa |
| --- | --- |
| Treino converge | `mAP@0.5` val sobe e estabiliza antes de época 100 |
| H1 | E01 mAP@0,5 ≥ 0,78 ou Recall ≥ 0,85 (referência REF Etapa 1) |
| Reprodutibilidade | Mesma seed → métricas similares (± pequena variação GPU) |
| Artefatos | `best.pt`, CSV e HTML de val arquivados |

---

## 10. Checklist pós-treino

- [ ] `best.pt` salvo e caminho registrado no log do experimento
- [ ] `results.csv` / curvas de loss e mAP exportadas
- [ ] Validação no split **correspondente** ao treino (não misturar S1 train com S2 val)
- [ ] Métricas P, R, mAP@0.5, mAP@0.5:0.95 na tabela consolidada
- [ ] REF avaliado no S1 para comparação justa
- [ ] Entrada na tabela do artigo ([templates/tabela_resultados_s1.csv](templates/tabela_resultados_s1.csv))
- [ ] Hiperparâmetros e versão `yolov5` documentados em `outputs/experiments/E01_*/experiment_log.txt`

---

## 11. Validação val degradado

E01 participa apenas do **val limpo** (S1, S2, S3). Val degradado reservado à comparação **E03 vs E04** (YOLO11 / YOLO11-R).

---

## 12. Tabelas e gráficos

| Artefato | Destino |
| --- | --- |
| Métricas E01 S1 | `templates/tabela_resultados_s1.csv` linha E01 |
| Métricas E05, E06 | `templates/tabela_splits.csv` |
| Barra G1 | Contribuição E01 no gráfico S1 |

---

## 13. Parágrafo de discussão (bullets)

- **H1:** E01 vs REF — cobertura e mAP.
- **H2a:** E01 como baseline v5 frente a E02.
- **H4:** E01 em S1/S2/S3 — efeito de mais dados de treino no Recall.

---

## 14. Checklist B+C (E01)

- [ ] Treino E01 concluído
- [ ] Val limpo + CSV
- [ ] Linha na tabela S1
- [ ] Citado na discussão §4 do artigo

---

## Referências rápidas

- Ultralytics YOLOv5: https://github.com/ultralytics/yolov5
- Métricas: [explicacao_metricas_yolov5](../entrega_parte_a/explicacao_metricas_yolov5_para_apresentacao.md)
- Plano 02 (YOLOv8s): [plano_02_yolov8_treino_padrao.md](plano_02_yolov8_treino_padrao.md)
- Plano 03 (YOLO11s): [plano_03_yolov11_treino_padrao.md](plano_03_yolov11_treino_padrao.md)
- Plano 04 (YOLO11-R): [plano_04_yolov11_r_robusto.md](plano_04_yolov11_r_robusto.md)
