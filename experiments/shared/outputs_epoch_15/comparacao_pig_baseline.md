# Comparação — dataset pig fixo (train/val Kaggle)

Modelos autorais E01–E03. Mesmo conjunto de **validação** (`pig/val`, 136 imagens).

| Modelo | Exp | Precision | Recall | mAP@0.50 | mAP@0.50:0.95 | F1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| YOLOv5s autoral | E01 | 0.9815 | 0.9637 | 0.9874 | 0.8043 | 0.9725 |
| YOLOv8s autoral | E02 | 0.9854 | 0.9797 | 0.9842 | 0.8083 | 0.9825 |
| YOLO11s autoral | E03 | 0.9790 | 0.9781 | 0.9839 | 0.8063 | 0.9785 |

## Tempo de validação

| Modelo | Exp | Total (s) | ms/img | device |
| --- | --- | ---: | ---: | --- |
| YOLOv5s autoral | E01 | 46.227 | 339.9 | 0 |
| YOLOv8s autoral | E02 | 16.326 | 120.0 | 0 |
| YOLO11s autoral | E03 | 16.469 | 121.1 | 0 |

## H1 — E02 vs E01 (YOLOv8 vs YOLOv5)

| Métrica | E02 | E01 | Δ (E02 − E01) |
| --- | ---: | ---: | ---: |
| Precision | 0.9854 | 0.9815 | +0.0039 |
| Recall | 0.9797 | 0.9637 | +0.0160 |
| mAP@0.50 | 0.9842 | 0.9874 | -0.0033 |
| mAP@0.50:0.95 | 0.8083 | 0.8043 | +0.0040 |
| F1 | 0.9825 | 0.9725 | +0.0100 |

## H2 — E03 vs E02 (YOLO11 vs YOLOv8)

| Métrica | E03 | E02 | Δ (E03 − E02) |
| --- | ---: | ---: | ---: |
| Precision | 0.9790 | 0.9854 | -0.0064 |
| Recall | 0.9781 | 0.9797 | -0.0016 |
| mAP@0.50 | 0.9839 | 0.9842 | -0.0002 |
| mAP@0.50:0.95 | 0.8063 | 0.8083 | -0.0020 |
| F1 | 0.9785 | 0.9825 | -0.0040 |

## Gráficos individuais

Um arquivo PNG por parâmetro em `experiments/shared/outputs/figures/`. Todos compartilham a mesma estrutura de barras.

### Eixos (todos os gráficos)

- **Eixo X:** Modelo treinado e validado no mesmo `pig/val` (136 imagens): **E01 YOLOv5s** (azul), **E02 YOLOv8s** (laranja), **E03 YOLO11s** (verde).
- **Eixo Y:** valor numérico da métrica ou do tempo medido na validação (rótulo *Valor* ou *Tempo* no gráfico).

### Métricas de detecção (série G1)

#### `G1_precision.png` — Precision

- **Arquivo:** `experiments/shared/outputs/figures/G1_precision.png`
- **O que mostra:** Das caixas preditas pelo modelo, qual fração está correta (IoU ≥ 0,50 com ground truth). Mede **confiabilidade** das detecções — poucos falsos positivos.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Valor — escala 0 a 1 (quanto maior, melhor)

#### `G1_recall.png` — Recall

- **Arquivo:** `experiments/shared/outputs/figures/G1_recall.png`
- **O que mostra:** Dos leitões anotados no ground truth, qual fração foi detectada. Mede **cobertura** — poucos falsos negativos (leitões não vistos).
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Valor — escala 0 a 1 (quanto maior, melhor)

#### `G1_map50.png` — mAP@0.50

- **Arquivo:** `experiments/shared/outputs/figures/G1_map50.png`
- **O que mostra:** Mean Average Precision com IoU mínimo de 0,50. Resume precisão e recall considerando o **ranking de confiança** das detecções.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Valor — escala 0 a 1 (quanto maior, melhor)

#### `G1_map50_95.png` — mAP@0.50:0.95

- **Arquivo:** `experiments/shared/outputs/figures/G1_map50_95.png`
- **O que mostra:** mAP médio em vários limiares de IoU (0,50 a 0,95). Métrica **mais exigente** que mAP@0,50 — penaliza caixas imprecisas mesmo quando a classe está correta.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Valor — escala 0 a 1 (quanto maior, melhor)

### Tempos de validação (série G2)

#### `G2_total_time_sec.png` — Tempo total de validação

- **Arquivo:** `experiments/shared/outputs/figures/G2_total_time_sec.png`
- **O que mostra:** Tempo do pipeline completo de validação: métricas globais + inferência por imagem + cálculo TP/FP/FN. Inclui `val` + `detect` + `match`.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Tempo (s) — escala Segundos (quanto menor, mais rápido)

#### `G2_ms_per_image.png` — Tempo por imagem

- **Arquivo:** `experiments/shared/outputs/figures/G2_ms_per_image.png`
- **O que mostra:** Custo médio por frame: `total_time_sec ÷ 136 × 1000`. Útil para comparar **velocidade em produção** (vídeo/tempo real).
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Tempo — escala Milissegundos por imagem (quanto menor, mais rápido)

#### `G2_val_time_sec.png` — Tempo do val

- **Arquivo:** `experiments/shared/outputs/figures/G2_val_time_sec.png`
- **O que mostra:** Tempo da etapa `model.val()` / `yolov5.val` — calcula precision, recall e mAP no conjunto de validação de uma vez.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Tempo (s) — escala Segundos (quanto menor, mais rápido)

#### `G2_detect_time_sec.png` — Tempo do detect

- **Arquivo:** `experiments/shared/outputs/figures/G2_detect_time_sec.png`
- **O que mostra:** Tempo da inferência imagem a imagem (`detect`) para gerar labels preditas usadas no CSV `per_image_tp_fp_fn.csv`.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Tempo (s) — escala Segundos (quanto menor, mais rápido)

#### `G2_match_time_sec.png` — Tempo do match

- **Arquivo:** `experiments/shared/outputs/figures/G2_match_time_sec.png`
- **O que mostra:** Tempo para comparar predições vs ground truth por imagem (IoU, TP/FP/FN). Etapa leve em CPU; não envolve rede neural.
- **Eixo X:** modelo (E01 / E02 / E03)
- **Eixo Y:** Tempo (s) — escala Segundos (quanto menor, mais rápido)

### Como ler

- Barras **mais altas** nos gráficos G1 indicam **melhor desempenho** de detecção.
- Barras **mais baixas** nos gráficos G2 indicam **validação mais rápida**.
- Compare sempre os três modelos no **mesmo gráfico** — mesma métrica, mesmo split, `conf=0,25`.

## O que significa cada métrica

Contexto: **detecção de objetos** em `pig/val`, 136 imagens, `conf=0,25`.

### Precision (P)

Das detecções emitidas pelo modelo, quantas caixas estão corretas (IoU ≥ 0,50 com algum ground truth).

### Recall (R)

Dos objetos anotados no ground truth, quantos foram detectados.

### F1

Média harmônica entre Precision e Recall — resume o equilíbrio entre acertar sem errar (P) e não deixar passar (R):

```
F1 = 2 × P × R / (P + R)
```

No pipeline, P e R vêm do `model.val()` (Ultralytics); F1 é calculado em `metrics_utils.f1_score` a partir desses valores (não é exportado diretamente pelo Ultralytics).

### mAP@0.50 / mAP@0.50:0.95

Métricas principais de detecção (consideram ranking de confiança e, no mAP@0.50:0.95, vários limiares de IoU). F1 complementa P e R, mas não substitui mAP na análise principal.

### Leitura rápida

- **mAP@0,50 ~0,99** — saturado para modelos maduros no pig/val.
- **F1 ~0,97–0,99** — próximo de P e R quando ambos são altos.
- Análise TCD: `entrega_parte_2/apoio_metricas.md`
