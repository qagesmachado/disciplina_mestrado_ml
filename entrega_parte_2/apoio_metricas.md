# Métricas de avaliação — detecção de leitões

Contexto: validação em `pig/val` (136 imagens), limiar de confiança `conf=0,25`, matching por IoU ≥ 0,50. Implementação de matching: `experiments/shared/scripts/metrics_utils.py`.

---

## 1. IoU (Intersection over Union)

Mede sobreposição entre caixa predita e ground truth:

```
IoU = área(Bp ∩ Bgt) / área(Bp ∪ Bgt)
```

Onde `Bp` = caixa predita e `Bgt` = caixa anotada (ground truth).

Uma predição conta como correta se IoU ≥ 0,50 e a classe coincide (`pig`).

---

## 2. TP, FP, FN

Por imagem, após ordenar predições por confiança:

- **TP (True Positive):** predição correta (classe + IoU ≥ 0,50), cada GT usado no máximo uma vez.
- **FP (False Positive):** predição sem GT correspondente.
- **FN (False Negative):** GT sem predição correspondente.

Agregados no conjunto de validação:

```
TP = Σ TP_i    (soma sobre todas as imagens i)
FP = Σ FP_i
FN = Σ FN_i
```

---

## 3. Precision (P)

```
P = TP / (TP + FP)
```

Fração das detecções emitidas que estão corretas. Alta precision → poucos falsos positivos (caixas espúrias).

---

## 4. Recall (R) — Revocação

```
R = TP / (TP + FN)
```

Fração dos leitões anotados que foram detectados. Alto recall → poucos objetos perdidos.

---

## 5. F1-Score

Média harmônica entre P e R:

```
F1 = 2 × P × R / (P + R)
```

Forma equivalente em termos de contagens:

```
F1 = 2 × TP / (2 × TP + FP + FN)
```

Calculado em `metrics_utils.f1_score()` a partir de P e R do `model.val()`. Resume equilíbrio P/R; **não substitui mAP** na análise principal.

---

## 6. AP@IoU (Average Precision)

Para cada classe, ordenam-se predições por confiança decrescente e constrói-se a curva Precision–Recall. AP é a **área sob essa curva** em um limiar de IoU fixo:

```
AP@t = área sob a curva P(R), de R=0 até R=1
```

(discretizado nas implementações práticas, como COCO e Ultralytics)

Com uma única classe (`pig`), AP@0,50 ≈ mAP@0,50.

---

## 7. mAP@0.50

```
mAP@0,50 = (1/C) × Σ AP@0,50 (classe c)    para c = 1 … C
```

Com C = 1 (só a classe `pig`), equivale ao AP com IoU = 0,50. Indica se o modelo **encontra** os objetos com caixa razoavelmente posicionada.

**Leitura no pig/val:** valores ~0,98–0,99 indicam **saturação** — pouco discriminativo entre modelos maduros.

---

## 8. mAP@0.50:0.95 (COCO)

Média do AP em dez limiares de IoU:

```
T = {0,50 ; 0,55 ; 0,60 ; 0,65 ; 0,70 ; 0,75 ; 0,80 ; 0,85 ; 0,90 ; 0,95}

mAP@0,50:0,95 = (1/10) × Σ AP@t    para t ∈ T
```

Métrica **mais rigorosa**: penaliza caixas mal alinhadas. Eixo principal para comparar E01, E02 e E03 neste TCD.

---

## 9. Tempo de inferência (complementar)

`ms/img` — tempo médio de validação por imagem. Relevante para comparar v5 (anchor-based, repo legado) vs Ultralytics (v8/v11 ~2,8–3× mais rápidos no hardware testado: 131,9 e 123,4 vs 372,1 ms/img).

---

## Métricas citadas no PDF da disciplina — por que não são principais aqui

| Métrica | Uso típico | Por que secundária neste TCD |
| --- | --- | --- |
| **Acurácia** | Classificação balanceada | Detecção densa: milhares de predições por imagem; acurácia global não reflete qualidade das caixas |
| **ROC-AUC** | Classificação binária | Detecção usa ranking PR por classe, não curva ROC como métrica padrão COCO |
| **MSE / MAE** | Regressão | Problema é localização + classificação, não regressão escalar |
| **Silhouette / Davies-Bouldin** | Clustering | Não há agrupamento não supervisionado no protocolo |

---

## Critérios de comparação entre modelos

1. **Primário:** mAP@0.50:0.95 no mesmo `pig/val`.
2. **Secundário:** Recall (cobertura em cenas densas), F1, tempo de inferência.
3. **Diagnóstico:** mAP@0.50 (saturado — interpretar com cautela).

Hipóteses desta entrega:

- **H1:** E02 ≥ E01 em mAP@0.50:0.95 → preliminar: **não confirmada** (E01 = 0,8302; E02 = 0,7986; Δ = −0,0316).
- **H2:** E03 ≥ E02 em mAP@0.50:0.95 → preliminar: **parcialmente confirmada** (mAP@0,50:0,95 Δ = +0,0039; F1 Δ = −0,0071).

Fonte numérica: [comparacao_pig_baseline.md](../experiments/shared/outputs/comparacao_pig_baseline.md).
