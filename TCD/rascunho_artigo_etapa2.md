# Reconhecimento de Leitões em Imagens: EDA, Metodologia Comparativa e Resultados com Detectores YOLO

Rascunho consolidado — Etapas B+C.  
Base: [Etapa1_GustavoMachado.doc](entrega%20parcial%201/Etapa1_GustavoMachado.doc).

Documentação: [entrega_parte_b_c/](../entrega_parte_b_c/).

---

## Abstract

Four author-trained detectors (YOLOv5s, YOLOv8s, YOLO11s, YOLO11-R) on 1065 piglet images with 80/20, 75/25, and 70/30 splits. External `best.pt` reference only. Metrics: P, R, mAP@0.50, mAP@0.50:0.95; degraded validation for YOLO11-R vs YOLO11s.

## Resumo

Quatro detectores autorais (YOLOv5s, YOLOv8s, YOLO11s, YOLO11-R) no dataset de leitões, com splits 80/20, 75/25 e 70/30. `best.pt` como referência externa. Metodologia e resultados documentados em [entrega_parte_b_c](../entrega_parte_b_c/plano_b_c.md).

---

## 1. Introdução

*(Etapa 1 — manter texto do .doc entregue.)*

---

## 2. Análise exploratória

*(Etapa 1.)* REF: P=0,650; R=0,854; mAP@0,50=0,785; mAP@0,50:0,95=0,273.

---

## 3. Metodologia

Texto: [entrega_parte_b_c/secao_metodologia_artigo.md](../entrega_parte_b_c/secao_metodologia_artigo.md)

- E01–E04 no S1; E05–E12 nos splits S2/S3
- Hipóteses H1–H4

---

## 4. Resultados e discussão

Texto: [entrega_parte_b_c/secao_resultados_discussao_artigo.md](../entrega_parte_b_c/secao_resultados_discussao_artigo.md)

Dados: [entrega_parte_b_c/templates/](../entrega_parte_b_c/templates/)

*(Preencher tabelas e figuras após treinos.)*

---

## 5. Considerações finais

Estudo comparativo de quatro gerações/protocolos YOLO com avaliação integrada de desempenho e robustez.

---

## Anexos

- [plano_b_c.md](../entrega_parte_b_c/plano_b_c.md)
- [protocolo](../entrega_parte_b_c/protocolo_splits_e_experimentos.md)
- [fluxograma B+C](../entrega_parte_b_c/fluxograma_b_c.md)
