# Reconhecimento de Leitões em Imagens: Metodologia e Desenho Experimental

**Gustavo E. S. Machado** — Faculdade de Engenharia Elétrica, UFU — gustavo.machado@ufu.br

---

## Abstract

This study extends the initial piglet detection investigation by defining a reproducible experimental methodology with three author-trained object detectors: YOLOv5s, YOLOv8s, and YOLO11s. All models are fine-tuned on the fixed Kaggle Pig Dataset partition (929 train / 136 validation images) and evaluated on the same validation set. Preliminary results show saturated mAP@0.50 (~0.98–0.99) and discriminative differences at mAP@0.50:0.95, where YOLOv5s (0.830) outperforms YOLO11s (0.803) and YOLOv8s (0.799). Ultralytics models (YOLOv8s/YOLO11s) achieve ~2.8–3× faster validation per image than YOLOv5s.

## Resumo

Este texto apresenta o desenho metodológico da Etapa 2 do TCD: três detectores autorais (YOLOv5s, YOLOv8s, YOLO11s) treinados no dataset pig fixo e avaliados no mesmo conjunto de validação. Define-se estratégia experimental hold-out, métricas de detecção e hipóteses comparativas. Resultados preliminares indicam saturação em mAP@0,50 e maior poder discriminativo em mAP@0,50:0,95, com YOLOv5s ligeiramente superior nas métricas rigorosas e modelos Ultralytics ~2,8–3× mais rápidos na inferência.

---

## 1. Introdução

A detecção de objetos em imagens é central em Visão Computacional, com aplicações em monitoramento inteligente e automação. No domínio de suinocultura de precisão, abordagens baseadas em YOLOv5 têm apresentado resultados promissores [Li and Li 2024; Peng et al. 2024].

No monitoramento de leitões em ambiente coletivo, os desafios incluem alta concentração de indivíduos por quadro, sobreposição entre corpos e variações de iluminação. A Etapa 1 caracterizou a base (1065 imagens, 11–15 leitões por cena, alta homogeneidade) e registrou um baseline exploratório com o modelo pré-treinado `best.pt` do dataset (Precision = 0,650; Recall = 0,854; mAP@0,50 = 0,785; mAP@0,50:0,95 = 0,273). Esse baseline **não compõe** os três algoritmos desta entrega — serve apenas como referência histórica da fase exploratória.

A presente etapa estrutura o fluxo experimental completo e compara três detectores autorais treinados pelo autor.

---

## 2. Análise exploratória (Etapa 1 — resumo)

Mantém-se da Etapa 1:

- **Base:** Kaggle Pig Dataset [ZIMANGE, s.d.], anotações YOLO, classe `pig`.
- **Partição:** 929 imagens de treino (≈80%) e 136 de validação (≈20%).
- **Densidade:** 11–15 leitões por imagem; moda em k=13 e k=14.
- **Verificação:** script Python para sobrepor bounding boxes e inspecionar consistência das anotações.

Detalhes, histogramas e Tabela 1: ver [Etapa1_GustavoMachado.pdf](../entrega_parte_1/Etapa1_GustavoMachado.pdf).

---

## 3. Metodologia

### 3.1 Base de dados e particionamento

Utiliza-se a partição **fixa** consolidada no repositório:

| Partição | Caminho | Imagens |
| --- | --- | ---: |
| Treino | `pig/train/images` | 929 |
| Validação | `pig/val/images` | 136 |

**Estratégia de validação:** hold-out — treino exclusivamente em `pig/train`; todas as métricas reportadas em `pig/val`. YAML: `experiments/data/yaml/pig_dataset.yaml`.

**Validade experimental:** mesmo conjunto de validação para E01, E02 e E03; `seed=42`; early stopping (`patience=20`) para mitigar overfitting.

### 3.2 Seleção dos algoritmos

Três detectores supervisionados, treinados pelo autor a partir de pesos COCO:

| ID | Modelo | Framework |
| --- | --- | --- |
| E01 | YOLOv5s | pacote `yolov5` |
| E02 | YOLOv8s | Ultralytics |
| E03 | YOLO11s | Ultralytics |

Justificativa detalhada, vantagens, limitações e hiperparâmetros: [apoio_algoritmos.md](apoio_algoritmos.md).

### 3.3 Estratégia experimental

**Hiperparâmetros compartilhados:** `imgsz=640`, `epochs=100`, `patience=20`, `seed=42`, variante `s`, augmentação padrão de cada framework, `conf=0,25` na validação.

**Ambientes isolados:**

- E01: `venv_yolo_5`
- E02/E03: `venv_yolo_ultralytics` (mesmo venv; só muda o arquivo de pesos)

**Reprodutibilidade:** scripts em `experiments/YOLO_V5/`, `YOLO_V8/`, `YOLO_V11/`; comparação via `experiments/shared/scripts/comparar.py`.

**Evitar overfitting:** conjunto de validação fixo e separado; early stopping; não ajustar hiperparâmetros com base repetida no val (treino único por modelo).

**Balanceamento de classes:** uma única classe (`pig`); não aplicável balanceamento entre classes.

### 3.4 Métricas de avaliação

**Principais:** Precision, Recall, mAP@0,50, mAP@0,50:0,95.  
**Complementares:** F1, tempo de validação por imagem (ms/img).

Equações e justificativa: [apoio_metricas.md](apoio_metricas.md).

### 3.5 Hipóteses

| ID | Hipótese | Critério |
| --- | --- | --- |
| H1 | YOLOv8s autoral ≥ YOLOv5s autoral | mAP@0,50:0,95 em `pig/val` |
| H2 | YOLO11s autoral ≥ YOLOv8s autoral | mAP@0,50:0,95 ou F1 |

---

## 4. Resultados preliminares

Avaliação no mesmo `pig/val` (136 imagens, `conf=0,25`). Fonte numérica: `experiments/shared/outputs/comparacao_pig_baseline.csv` (experimentos E01–E03; valores do `model.val()` / `yolov5.val`).

### 4.1 Métricas de detecção

| Modelo | Exp | Precision | Recall | mAP@0,50 | mAP@0,50:0,95 | F1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| YOLOv5s autoral | E01 | **0,9918** | 0,9776 | **0,9914** | **0,8302** | 0,9846 |
| YOLOv8s autoral | E02 | 0,9915 | **0,9803** | 0,9845 | 0,7986 | **0,9858** |
| YOLO11s autoral | E03 | 0,9865 | 0,9712 | 0,9833 | 0,8025 | 0,9788 |

**Figuras (uma por métrica):** `experiments/shared/outputs/figures/G1_precision.png`, `G1_recall.png`, `G1_map50.png`, `G1_map50_95.png`.

### 4.2 Tempo de validação

| Modelo | Exp | Total (s) | ms/img | device |
| --- | --- | ---: | ---: | ---: |
| YOLOv5s autoral | E01 | 50,6 | 372,1 | 0 |
| YOLOv8s autoral | E02 | 17,9 | 131,9 | 0 |
| YOLO11s autoral | E03 | 16,8 | **123,4** | 0 |

**Figuras:** `experiments/shared/outputs/figures/G2_ms_per_image.png`, `G2_total_time_sec.png` (complementares: `G2_val_time_sec.png`, `G2_detect_time_sec.png`, `G2_match_time_sec.png`).

### 4.3 Interpretação

- **mAP@0,50 saturado (~0,98–0,99):** diferenças pequenas; pouco discriminativo entre modelos maduros nesta base homogênea.
- **mAP@0,50:0,95 (métrica principal):** ranking E01 (0,8302) > E03 (0,8025) > E02 (0,7986). O YOLOv5s mantém caixas mais bem alinhadas sob limiares de IoU mais rígidos.
- **F1:** ranking E02 (0,9858) ≳ E01 (0,9846) > E03 (0,9788). O equilíbrio P/R é praticamente empatado entre v5 e v8.
- **H1 (E02 ≥ E01 em mAP@0,50:0,95):** **não confirmada** — v8 ficou abaixo de v5 (Δ = −0,0316).
- **H2 (E03 ≥ E02):** **parcialmente confirmada** — v11 supera v8 em mAP@0,50:0,95 (Δ = +0,0039), mas não em F1 (Δ = −0,0071).
- **Inferência:** modelos Ultralytics (E02/E03) são **~2,8–3×** mais rápidos por imagem que o YOLOv5s (E01: 372,1 ms/img vs 131,9 e 123,4 ms/img).

### 4.4 Deltas por hipótese

| Métrica | H1: E02 − E01 | H2: E03 − E02 |
| --- | ---: | ---: |
| Precision | −0,0003 | −0,0050 |
| Recall | +0,0027 | −0,0091 |
| mAP@0,50 | −0,0069 | −0,0012 |
| mAP@0,50:0,95 | −0,0316 | +0,0039 |
| F1 | +0,0012 | −0,0071 |

Tabela completa e gráficos: [comparacao_pig_baseline.md](../experiments/shared/outputs/comparacao_pig_baseline.md).

---

## 5. Dificuldades encontradas

1. **Saturação de métricas** no val limpo — dificulta distinguir modelos só por mAP@0,50; a comparação principal recai sobre mAP@0,50:0,95.
2. **Dois ambientes Python** (`venv_yolo_5` e `venv_yolo_ultralytics`) — necessário para não misturar dependências incompatíveis entre o repositório YOLOv5 legado e o Ultralytics.
3. **PyTorch/GPU no Windows** — instalação padrão via pip traz torch CPU-only; exige script de setup para CUDA.
4. **Homogeneidade da base** — baixa variabilidade de densidade limita generalização de conclusões sobre robustez.

---

## 6. Próximos passos

- Análise qualitativa de FP/FN em cenas densas (11–15 leitões), usando os recortes `val_batch*_pred.jpg` de cada experimento.
- Estudos opcionais de robustez (validação degradada: brilho, desfoque, ruído).
- Sensibilidade a splits alternativos (fora do escopo desta entrega).
- Consolidação do artigo final e discussão frente à literatura.

---

## Referências

- L. Li and F. Li, "Pig Detection Method Based on Improved YOLOv5," ISDH 2024.
- N. Peng, F. Li and X. Luo, "PLM-YOLOv5: Improved YOLOv5 for Pig Detection in Livestock Monitoring," IRAC 2024.
- ULTRALYTICS. YOLOv5. GitHub, 2022. https://github.com/ultralytics/yolov5
- ULTRALYTICS. Documentação Ultralytics. https://docs.ultralytics.com/pt/quickstart
- ZIMANGE. Kaggle Pig Dataset. https://www.kaggle.com/datasets (acesso conforme Etapa 1).

---

*Fluxograma metodológico: [fluxograma.md](fluxograma.md)*
