# Protocolo de Splits e Experimentos — Parte B+C

> **Obsoleto para execução atual.** A proposta vigente usa o dataset **pig fixo** (train/val Kaggle): [protocolo_pig_fixo.md](protocolo_pig_fixo.md).

Documento de referência histórica para particionamento customizado S1–S3 e matriz **E01–E12**.

**Índice mestre:** [plano_b_c.md](plano_b_c.md).

**Referências:** [Etapa 1](../TCD/entrega%20parcial%201/Etapa1_GustavoMachado.doc), [rascunho Etapa 1](../TCD/rascunho_artigo_etapa1.md), [EDA Parte A](../entrega_parte_a/roteiro_slides_parte_a.md).

---

## 1. Pool de dados unificado

| Item | Valor |
| --- | --- |
| Dataset | Kaggle Pig Dataset (`pig/`) |
| Total de imagens | **1065** |
| Formato | YOLO, classe `pig` (id 0) |
| Densidade típica | 11–15 leitões por imagem |

---

## 2. Cenários de particionamento

| Cenário | Código | Train | Val |
| --- | --- | --- | --- |
| S1 | `80_20` | 852 | 213 |
| S2 | `75_25` | 799 | 266 |
| S3 | `70_30` | 746 | 319 |

`seed = 42`; pares imagem–label sempre juntos.

---

## 3. Matriz de experimentos (4 modelos autorais)

### Fase 1 — Split S1 (prioridade)

| ID | Modelo | Pesos iniciais | Framework | Plano |
| --- | --- | --- | --- | --- |
| **E01** | YOLOv5s | `yolov5s.pt` | `yolov5` (PyPI) | [plano_01](plano_01_yolov5_treino_proprio.md) |
| **E02** | YOLOv8s | `yolov8s.pt` | Ultralytics | [plano_02](plano_02_yolov8_treino_padrao.md) |
| **E03** | YOLO11s | `yolo11s.pt` | Ultralytics | [plano_03](plano_03_yolov11_treino_padrao.md) |
| **E04** | YOLO11-R | `yolo11s.pt` + aug robusta | Ultralytics | [plano_04](plano_04_yolov11_r_robusto.md) |

### Fase 2 — Sensibilidade ao split (S2, S3)

| ID | Modelo | Split |
| --- | --- | --- |
| E05 | YOLOv5s | S2 75/25 |
| E06 | YOLOv5s | S3 70/30 |
| E07 | YOLOv8s | S2 |
| E08 | YOLOv8s | S3 |
| E09 | YOLO11s | S2 |
| E10 | YOLO11s | S3 |
| E11 | YOLO11-R | S2 |
| E12 | YOLO11-R | S3 |

### Referência externa

| ID | Modelo | Uso |
| --- | --- | --- |
| **REF** | `pig/best.pt` | Terceiros; avaliar no **S1**; **não** é peso inicial |

---

## 4. Hiperparâmetros comuns

| Parâmetro | Valor |
| --- | --- |
| `imgsz` | 640 |
| `epochs` | 100 |
| `patience` | 20 |
| `seed` | 42 |
| `conf_thres` | 0.25 |
| Variante | `s` (small) em todos |

**Exceção:** augmentações do **YOLO11-R (E04, E11, E12)** — ver [plano_04](plano_04_yolov11_r_robusto.md).

---

## 5. Métricas (detecção — prioridade para artigo e rubrica C)

### Primárias (tabela mestra)

| Métrica | Uso |
| --- | --- |
| **mAP@0.50** | Desempenho global de detecção |
| **mAP@0.50:0.95** | Qualidade da localização das caixas |
| **Precision (P)** | Falsos positivos em cena densa |
| **Recall (R)** | Cobertura dos leitões anotados |

### Secundárias (discussão)

| Métrica | Uso |
| --- | --- |
| **F1** | Trade-off P×R |
| **TP, FP, FN / imagem** | Diagnóstico qualitativo |
| **Erro de contagem** | \|#detecções − #gabarito\| por imagem |
| **Queda relativa** | Robustez: E03 vs E04 no val degradado |

*Não usar como principal:* acurácia de classificação, silhueta, R².

---

## 6. Hipóteses

| ID | Hipótese |
| --- | --- |
| **H1** | E01–E04 ≥ REF em mAP@0,5 ou Recall no S1 |
| **H2a** | E02 ≥ E01 (v8 vs v5) no val limpo |
| **H2b** | E03 ≥ E02 (v11 vs v8) no val limpo |
| **H3** | E04 menor queda relativa que E03 no val degradado |
| **H4** | Mais dados de treino (S3→S2→S1) favorece Recall |

---

## 7. Ordem de execução (ciclo B+C por experimento)

Para cada **E0X**: treinar → val limpo → (se E03/E04) val degradado → exportar CSV → linha nas tabelas `templates/` → bullets de discussão no plano 0X §13.

1. Gerar splits S1–S3 + YAMLs  
2. **Fase 1:** E01 → E02 → E03 → E04 (S1)  
3. REF no S1  
4. Val degradado E03 vs E04 → `tabela_robustez.csv` + figura G3  
5. **Fase 2:** E05–E12 conforme GPU/tempo  
6. Consolidar: `tabela_resultados_s1.csv`, `tabela_splits.csv`, gráficos G1–G4  
7. Redigir [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md)

---

## 8. Protocolo de avaliação e consolidação (rubrica C)

### Mínimo para seminário B+C

- E01–E04 + REF no S1 com P, R, mAP@0,5, mAP@0,5:0,95  
- Gráfico G1 (barras)  
- Val degradado E03 vs E04 + discussão H3  
- Slides [roteiro_slides_b_c.md](roteiro_slides_b_c.md)

### Completo para artigo

- E05–E12 + gráfico G2 (splits)  
- Figuras qualitativas TP/FP/FN (G5–G6)  
- [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md) integral

---

## 9. Saídas

```
experiments/outputs/
  E01_yolov5s_80_20/
  E02_yolov8s_80_20/
  E03_yolo11s_80_20/
  E04_yolo11r_80_20/
  REF_best_pt_S1_80_20/
```

Splits e YAMLs: `experiments/data/` — gerar com `python experiments/scripts/gerar_splits.py`.
