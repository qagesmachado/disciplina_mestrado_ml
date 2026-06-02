# Roteiro de slides — Etapa 2 (~10 min + 5 min discussão)

**Título:** Metodologia e Desenho Experimental — Detecção de Leitões com YOLOv5, YOLOv8 e YOLO11

---

## Slide 1 — Título

- Nome, UFU, disciplina
- Etapa 2: Metodologia e Desenho da Pesquisa

## Slide 2 — Contextualização do problema (PDF §1)

- Detecção de leitões em cenas densas (11–15 por imagem)
- Etapa 1: base Kaggle, análise exploratória
- Baseline histórico `best.pt` (Etapa 1): P=0,650; mAP@0,50=0,785 — **fora** da comparação principal

## Slide 3 — Fluxograma metodológico (PDF §2)

- Figura: exportar de [fluxograma.md](fluxograma.md)
- Hold-out fixo; três treinos autorais; avaliação única em `pig/val`

## Slide 4 — Algoritmos: visão geral (PDF §3)

- Tabela: YOLOv5s (E01) | YOLOv8s (E02) | YOLO11s (E03)
- Três algoritmos supervisionados; pesos COCO; checkpoints autorais

## Slide 5 — Algoritmos: justificativa (PDF §3)

- v5: baseline literatura suínos
- v8: geração intermediária Ultralytics
- v11: geração atual
- Detalhes: [apoio_algoritmos.md](apoio_algoritmos.md)

## Slide 6 — Estratégia experimental (PDF §4)

- Hold-out 929/136; `seed=42`; `patience=20`
- Dois venvs isolados; augmentação padrão de cada framework
- Evitar overfitting: val fixo + early stopping

## Slide 7 — Métricas de avaliação (PDF §5)

- P = TP/(TP+FP); R = TP/(TP+FN); F1 = 2PR/(P+R)
- mAP@0,50 (saturado) vs mAP@0,50:0,95 (eixo principal)
- Detalhes: [apoio_metricas.md](apoio_metricas.md)

## Slide 8 — Resultados preliminares (PDF §6)

- Tabela E01–E03
- Figuras: `G1_map50_95.png`, `G1_precision.png`, `G1_recall.png`, `G1_map50.png` (tempo: `G2_ms_per_image.png`)
- H1 não confirmada (Δ mAP@0,50:0,95 = −0,0316); H2 parcialmente confirmada (+0,0039 em mAP, −0,0071 em F1)
- v8/v11 ~2,8–3× mais rápidos por imagem

## Slide 9 — Dificuldades encontradas (PDF §7)

- Saturação mAP@0,50
- GPU/PyTorch no Windows
- Dois ambientes Python
- Base homogênea

## Slide 10 — Próximos passos (PDF §8)

- Análise FP/FN qualitativa
- Robustez (opcional, futuro)
- Artigo final

---

## Notas para apresentação

- Priorizar **mAP@0.50:0.95** na fala (não mAP@0.50).
- Mencionar `best.pt` só como contexto da Etapa 1.
- Tempo sugerido: ~1 min/slide.
