# Especificação de gráficos — Parte B+C

Preencher após treinos; exportar PNG para slides e artigo.

---

## Figura G1 — Barras: métricas no pig/val (obrigatório seminário)

| Item | Detalhe |
| --- | --- |
| Dados | `templates/tabela_resultados_s1.csv` ou `comparar.py` |
| Eixo X | E01, E02 (quando validado), E03, E04, REF |
| Eixo Y | Precision, Recall, mAP@0,50, mAP@0,50:0,95 |
| Título | Comparação de detectores no `pig/val` (136 imgs) |
| Arquivo saída | `experiments/shared/outputs/figures/G1_pig_baseline.png` |

---

## Figura G2 — Linhas: sensibilidade ao split (artigo completo)

| Item | Detalhe |
| --- | --- |
| Dados | `templates/tabela_splits.csv` |
| Linhas | Uma por modelo (v5, v8, v11, v11-R) |
| Eixo X | % treino (70, 75, 80) |
| Métrica | Recall ou mAP@0,50 |
| Arquivo | `outputs/figures/G2_splits_recall.png` |

---

## Figura G3 — Robustez: queda relativa (obrigatório H3)

| Item | Detalhe |
| --- | --- |
| Dados | `templates/tabela_robustez.csv` |
| Comparar | E03 vs E04 |
| Eixo X | Cenário degradado |
| Eixo Y | Queda relativa mAP@0,50 (%) |
| Arquivo | `outputs/figures/G3_robustez_queda_map50.png` |

---

## Figura G4 — Curvas de treino (por experimento)

| Item | Detalhe |
| --- | --- |
| Fonte | `outputs/experiments/E0X_*/results.png` ou `results.csv` |
| Painéis | loss, mAP@0,5 val — um painel por modelo na Fase 1 |
| Arquivo | `outputs/figures/G4_curvas_treino_fase1.png` |

---

## Figura G5–G6 — Qualitativo TP/FP/FN (artigo)

| Item | Detalhe |
| --- | --- |
| Conteúdo | 2–3 imagens: acerto típico, FP em cena densa, FN |
| Fonte | `val_batch*_pred.jpg` ou script de overlay |
| Arquivos | `G5_exemplo_tp.png`, `G6_exemplo_fp_fn.png` |

---

## Checklist de figuras para apresentação

- [ ] G1 no slide de resultados
- [ ] G3 no slide de robustez (após val degradado)
- [ ] Fluxograma de [fluxograma_b_c.md](../fluxograma_b_c.md)
