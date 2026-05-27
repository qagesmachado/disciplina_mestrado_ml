# Seção 3 — Metodologia (texto para o artigo)

Base: [Etapa1_GustavoMachado.doc](../TCD/entrega%20parcial%201/Etapa1_GustavoMachado.doc). Seções 1–2 permanecem da Etapa 1.

---

## 3. Metodologia

O procedimento foi organizado em: (i) repartição da base; (ii) **quatro detectores** treinados pelo autor, cobrindo gerações YOLOv5, YOLOv8 e YOLO11 e um protocolo adaptado de robustez; (iii) variável de split treino/validação; (iv) métricas de detecção e avaliação degradada.

### 3.1 Base de dados e particionamento

Utilizou-se o Kaggle Pig Dataset (**1065 imagens**, formato YOLO, classe `pig`), com a partição **fixa** já fornecida pela fonte e consolidada no repositório:

| Partição | Imagens (aprox.) |
| --- | --- |
| Treino (`pig/train`) | 929 |
| Validação (`pig/val`) | 136 |

Todos os experimentos autorais (E01, E02, …) e a referência externa (REF) são avaliados no **mesmo** conjunto de validação, garantindo comparabilidade direta. Análises de sensibilidade a splits alternativos (80/20, 75/25, 70/30) permanecem como estudo futuro opcional (documentação legada).

### 3.2 Algoritmos selecionados

Foram treinados **quatro detectores autorais** (pesos iniciais COCO, checkpoints finais próprios):

1. **YOLOv5s** — baseline alinhada à literatura de suínos [Li and Li 2024; Peng et al. 2024] e à Etapa 1 (`yolov5s.pt`, framework YOLOv5).

2. **YOLOv8s** — geração intermediária Ultralytics, augmentação padrão (`yolov8s.pt`), para comparar evolução em relação ao v5.

3. **YOLO11s** — geração atual estável no ecossistema [Ultralytics](https://github.com/ultralytics/ultralytics) (`yolo11s.pt`), augmentação padrão.

4. **YOLO11-R** — mesmo backbone que o YOLO11s, com **protocolo de treino adaptado**: HSV e transformações geométricas reforçadas, mixup, copy-paste (cenas densas) e simulação de desfoque/ruído no treino, motivado por trabalhos de robustez em detecção de suínos, sem reimplementar módulos proprietários (ex.: PLM-YOLOv5).

**Referência externa:** `best.pt` do dataset — apenas comparação (Etapa 1: P=0,650; R=0,854; mAP@0,50=0,785; mAP@0,50:0,95=0,273). Não utilizado como peso inicial.

### 3.3 Protocolo e métricas

Hiperparâmetros compartilhados: `imgsz=640`, até 100 épocas, `patience=20`, `seed=42`, variante `s`, `conf=0,25`. Experimentos E01–E04 no S1; E05–E12 nos demais splits.

**Métricas principais:** Precision, Recall, mAP@0,50, mAP@0,50:0,95. **Complementares:** F1, TP/FP/FN por imagem, erro de contagem, queda relativa no conjunto de validação degradado (brilho, desfoque ou ruído) para comparar YOLO11s e YOLO11-R.

Detalhamento: [protocolo_pig_fixo.md](protocolo_pig_fixo.md) e planos [01](plano_01_yolov5_treino_proprio.md)–[04](plano_04_yolov11_r_robusto.md). Resultados e discussão: [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md). Cronograma: [plano_b_c.md](plano_b_c.md).

### 3.4 Hipóteses

- **H1:** Modelos autorais (E01–E04) ≥ REF no S1.  
- **H2a/b:** Progressão v5 → v8 → v11 no val limpo.  
- **H3:** YOLO11-R menor degradação que YOLO11s no val degradado.  
- **H4:** Maior fração de treino melhora Recall.

---

## Abstract (trecho EN)

Four detectors were trained on 1065 annotated piglet images: YOLOv5s, YOLOv8s, YOLO11s, and YOLO11-R (domain-oriented training on YOLO11s). Splits 80/20, 75/25, and 70/30 with fixed seed. A third-party `best.pt` is external reference only. Metrics: Precision, Recall, mAP@0.50, mAP@0.50:0.95, plus degraded-validation robustness for YOLO11-R.
