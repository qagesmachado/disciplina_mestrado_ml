# Plano B+C — dataset pig fixo (proposta atual)

**Escopo:** particionamento fixo `pig/train` + `pig/val` (Kaggle). Comparações **E01 vs REF (H1)** e **E02 vs E01 (H2a)**.

Protocolo: [protocolo_pig_fixo.md](protocolo_pig_fixo.md). Execução: [../experiments/README.md](../experiments/README.md).

---

## 1. Visão geral

| Rubrica | Foco atual |
| --- | --- |
| B | Metodologia: detectores autorais + REF, mesmo val |
| C | Tabela + gráfico + discussão H1 e H2a |

## 2. Modelos

| ID | Modelo | Venv | Plano | Status |
| --- | --- | --- | --- | --- |
| E01 | YOLOv5s autoral | `venv_yolo_5` | [plano_01](plano_01_yolov5_treino_proprio.md) | Concluído |
| E02 | YOLOv8s autoral | `venv_yolo_ultralytics` | [plano_02](plano_02_yolov8_treino_padrao.md) | Em execução |
| REF | `pig/best.pt` | `venv_yolo_5` | [protocolo_pig_fixo](protocolo_pig_fixo.md) | Validado |

Fase futura: E03–E04 (planos 03–04).

## 3. Hipóteses

| ID | Hipótese | Artefato |
| --- | --- | --- |
| H1 | E01 ≥ REF | [comparacao_pig_baseline.md](../experiments/shared/outputs/comparacao_pig_baseline.md) |
| H2a | E02 ≥ E01 | Mesmo arquivo (após validar E02) |

## 4. Cronograma

- [x] Baseline E01 + REF (`YOLO_V5/run_pig_baseline.ps1`)
- [ ] `YOLO_V8/setup_venv_ultralytics.ps1`
- [ ] Treino + val E02 (`YOLO_V8/run_yolov8_pig.ps1`)
- [ ] `comparar.py` com três modelos
- [ ] Slides / artigo

## 5. Artefatos

| Tipo | Arquivo |
| --- | --- |
| Comparação | `experiments/shared/outputs/comparacao_pig_baseline.md` |
| Gráfico | `experiments/shared/outputs/figures/G1_pig_baseline.png` |
| Tabela | [templates/tabela_resultados_s1.csv](templates/tabela_resultados_s1.csv) |
| Análise | [analise_desempenho_baseline.md](analise_desempenho_baseline.md) |

---

Documentos legados (splits S1–S3): [protocolo_splits_e_experimentos.md](protocolo_splits_e_experimentos.md) — **obsoleto**.
