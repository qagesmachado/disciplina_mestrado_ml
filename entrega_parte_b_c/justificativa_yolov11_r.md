# Justificativa do YOLO11-R (detector adaptado para robustez)

Documento de apoio ao [Plano 04](plano_04_yolov11_r_robusto.md).

---

## 1. Por que quatro detectores (v5, v8, v11, v11-R)?

A rubrica exige **no mínimo três** algoritmos; o desenho ampliado compara **gerações YOLO** e um **protocolo adaptado**:

| # | Modelo | Papel |
| --- | --- | --- |
| 1 | YOLOv5s | Baseline alinhada à literatura de suínos e à Etapa 1 |
| 2 | YOLOv8s | Geração intermediária (Ultralytics) |
| 3 | YOLO11s | Geração atual estável no [Ultralytics](https://github.com/ultralytics/ultralytics) |
| 4 | **YOLO11-R** | Mesmo backbone que (3), com **método adicional** de treino para robustez |

O YOLO11-R não é um quinto backbone: é **YOLO11s + protocolo de augmentação** (copy-paste, HSV, mixup, degradações simuladas no treino).

---

## 2. Por que YOLO11-R e não YOLOv8-R?

- O comparador “moderno padrão” passa a ser **YOLO11s** (E03), recomendado na documentação Ultralytics para uso estável.
- A adaptação robusta aplica-se à **geração mais recente** do pipeline unificado (`ultralytics`), facilitando manutenção e reprodutibilidade.
- **YOLOv8s (E02)** permanece para análise **v5 → v8 → v11** sem misturar efeito de protocolo robusto na geração 8.

---

## 3. Evidências da Etapa 1

- Alta densidade (11–15 leitões/imagem) → **copy-paste** no treino.
- mAP@0,50 alto e mAP@0,50:0,95 baixo no `best.pt` → métricas de localização fina são críticas.
- Recall alto, Precision moderada → robustez e FP relevantes na discussão.

---

## 4. Relação com a literatura

| Trabalho | Tradução no YOLO11-R |
| --- | --- |
| Li & Li (2024) — Improved YOLOv5 | Augmentações de domínio no treino |
| Peng et al. (2024) — PLM-YOLOv5 | Inspiração conceitual; sem reimplementar PLM |

---

## 5. Hipótese testável

> **H3:** Em validação degradada, **YOLO11-R (E04)** apresenta menor queda relativa de mAP@0,50 e Recall que **YOLO11s (E03)**, com desempenho equivalente no val limpo.

---

## 6. Texto sugerido para slide

"O YOLO11-R utiliza o mesmo YOLO11s dos experimentos padrão, com protocolo de augmentação orientado a granjas e cenas densas, incluindo copy-paste e simulação de degradações no treino, inspirado em trabalhos recentes de detecção de suínos."
