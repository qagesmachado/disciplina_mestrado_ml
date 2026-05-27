# Roteiro de Slides — Parte B+C (TCD)

**Título:** Metodologia, Resultados e Discussão — YOLOv5, v8, v11 e YOLO11-R para Detecção de Leitões  
**Pontuação:** B (20) + C (30) = **50 pts**  
**Mestre:** [plano_b_c.md](plano_b_c.md)

---

## Parte B — Metodologia (slides 1–9)

### Slide 1 — Título
- Parte B+C unificada
- Quatro detectores autorais + REF

### Slide 2 — Etapa 1
- 1065 imgs, densidade 11–15 leitões
- `best.pt` = terceiros (só REF)

### Slide 3 — Questão de pesquisa
> Evolução v5→v8→v11 e efeito do YOLO11-R sob splits e degradações?

### Slide 4 — Fluxograma B+C
- Figura: [fluxograma_b_c.md](fluxograma_b_c.md)

### Slide 5 — Splits S1/S2/S3
- Tabela 80/20, 75/25, 70/30
- Fase 1: E01–E04 | Fase 2: E05–E12

### Slide 6 — YOLOv5s (E01)
- [plano_01](plano_01_yolov5_treino_proprio.md)

### Slide 7 — YOLOv8s (E02)
- [plano_02](plano_02_yolov8_treino_padrao.md)

### Slide 8 — YOLO11s (E03)
- [plano_03](plano_03_yolov11_treino_padrao.md)

### Slide 9 — YOLO11-R (E04)
- [plano_04](plano_04_yolov11_r_robusto.md) | [justificativa](justificativa_yolov11_r.md)

---

## Ponte — Protocolo e métricas (slide 10)

| Métricas primárias | mAP@0,5, mAP@0,5:0,95, P, R |
| Secundárias | F1, TP/FP/FN, erro contagem, queda relativa |

[protocolo](protocolo_splits_e_experimentos.md) §5

---

## Parte C — Resultados (slides 11–14)

### Slide 11 — Tabela S1 (placeholder ou preenchida)
- E01–E04 + REF
- Fonte: [templates/tabela_resultados_s1.csv](templates/tabela_resultados_s1.csv)
- **Figura G1:** barras mAP@0,5

### Slide 12 — Progressão v5 → v8 → v11
- Comentar H2a, H2b com valores da tabela
- Opcional: curvas de treino (G4)

### Slide 13 — Robustez E03 vs E04
- Val degradado: brilho, blur, ruído
- **Figura G3:** queda relativa (H3)
- Fonte: [templates/tabela_robustez.csv](templates/tabela_robustez.csv)

### Slide 14 — Sensibilidade ao split (se E05–E12 executados)
- Figura G2 ou tabela resumida
- H4

---

## Discussão e fechamento (slides 15–17)

### Slide 15 — Discussão crítica
- Trade-offs densidade / FP / FN
- H1: autoral vs REF
- Limitações (base, tempo GPU)

### Slide 16 — Literatura
- Li 2024; Peng 2024
- YOLO11-R como protocolo, não PLM completo

### Slide 17 — Checklist B+C
- [checklist_rubrica_b_c.md](checklist_rubrica_b_c.md)

---

## Materiais de apoio

- [secao_metodologia_artigo.md](secao_metodologia_artigo.md)
- [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md)
- Planos 01–04
