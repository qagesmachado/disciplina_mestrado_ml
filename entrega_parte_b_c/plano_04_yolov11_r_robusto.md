# Plano 04 — YOLO11-R: YOLO11s com protocolo de adaptação para robustez

> **Execução futura:** mesmo padrão do E02 — **pig fixo**, `venv_yolo_ultralytics`. Splits S1–S3 abaixo são legado.

Quarto detector: **mesmo backbone** que o Plano 03 (`yolo11s.pt`), com **protocolo de treino adaptado** (augmentação de domínio + copy-paste) inspirado em [Li and Li 2024; Peng et al. 2024].

**Matriz:** E04 (S1), E11 (S2), E12 (S3).

**Documento complementar:** [justificativa_yolov11_r.md](justificativa_yolov11_r.md).

---

## 1. Objetivo e hipótese

**Objetivo:** maximizar robustez (iluminação, desfoque, ruído) via augmentações no **treino**, comparável a E03 no val limpo.

**Hipótese (H3):** no val **degradado**, E04 apresenta **menor queda relativa** de mAP@0,50 e Recall que E03; no val **limpo**, desempenho similar.

---

## 2. Pré-requisitos

Igual ao [Plano 03](plano_03_yolov11_treino_padrao.md), mais:

| Item | Detalhe |
| --- | --- |
| Config | `entrega_parte_b_c/config/yolo11r_hyp.yaml` (a criar na execução) |
| Opcional | `albumentations` para blur/ruído no treino |

---

## 3. Dados

| Experimento | YAML | Train / Val |
| --- | --- | --- |
| E04 | `data/yaml/data_split_80_20.yaml` | 852 / 213 |
| E11 | `data/yaml/data_split_75_25.yaml` | 799 / 266 |
| E12 | `data/yaml/data_split_70_30.yaml` | 746 / 319 |

---

## 4. Configuração de treino

### 4.1 Hiperparâmetros compartilhados com E03

| Parâmetro | Valor |
| --- | --- |
| `model` | `yolo11s.pt` |
| `imgsz` | 640 |
| `epochs` | 100 |
| `batch` | 16 ou 8 |
| `patience` | 20 |
| `seed` | 42 |

### 4.2 Adaptações YOLO11-R (diff vs E03)

| Parâmetro / técnica | E03 YOLO11s | E04 YOLO11-R |
| --- | --- | --- |
| `hsv_h` | default | **0.03** |
| `hsv_s` | default | **0.8** |
| `hsv_v` | default | **0.5** |
| `degrees` | default | **10.0** |
| `translate` | default | **0.15** |
| `scale` | default | **0.6** |
| `mixup` | default | **0.1** |
| `copy_paste` | default | **0.3** |
| Blur / ruído (treino) | não | **sim** |
| Literatura | — | Li 2024; Peng PLM-YOLOv5 2024 |

---

## 5. Comandos previstos (execução futura)

### E04 — treino S1

```powershell
yolo detect train ^
  model=yolo11s.pt ^
  data=data/yaml/data_split_80_20.yaml ^
  imgsz=640 ^
  epochs=100 ^
  batch=16 ^
  patience=20 ^
  seed=42 ^
  hsv_h=0.03 hsv_s=0.8 hsv_v=0.5 ^
  degrees=10 translate=0.15 scale=0.6 ^
  mixup=0.1 copy_paste=0.3 ^
  project=outputs/experiments ^
  name=E04_yolo11r_80_20 ^
  exist_ok=True
```

### E11, E12 — Fase 2

- `E11_yolo11r_75_25`, `E12_yolo11r_70_30`

---

## 6. Validação

**Val limpo:** igual aos demais (`conf=0.25`).

**Val degradado:** comparar E03 vs E04 nos mesmos cenários (brilho, blur, ruído); calcular queda relativa de mAP@0,5 e Recall.

---

## 7. Saídas esperadas

`outputs/experiments/E04_yolo11r_80_20/` + `robustez_comparativa.csv` (E03 vs E04).

---

## 8. Comparação

| Par | Foco |
| --- | --- |
| E04 vs E03 | H3 — protocolo robusto |
| E04 vs E02/E01 | Melhor configuração autoral vs gerações anteriores |
| vs REF | Referência externa |

---

## 9. Critérios de sucesso

- H3: queda relativa E04 < E03 no val degradado
- `copy_paste` confirmado em `args.yaml`

---

## 10. Checklist pós-treino

- [ ] E03 treinado antes
- [ ] Val limpo + val degradado
- [ ] Discussão no artigo ([secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md))

---

## 11. Validação val degradado

Mesmos cenários que E03 (Plano 03 §11). **Mesmas imagens degradadas** para comparação justa.

Calcular queda relativa e preencher `templates/tabela_robustez.csv` linhas E04.

Exportar `outputs/experiments/robustez_comparativa.csv` com colunas: modelo, cenario, map50, queda_map50, queda_recall.

---

## 12. Tabelas e gráficos

| Artefato | Destino |
| --- | --- |
| E04 S1 | `templates/tabela_resultados_s1.csv` |
| E11, E12 | `templates/tabela_splits.csv` |
| Robustez | `templates/tabela_robustez.csv` |
| **G3** | Figura principal H3 (E03 vs E04) |

---

## 13. Parágrafo de discussão

- **H3:** E04 menor queda que E03 — protocolo copy-paste e aug de domínio.
- Comparar mAP@0,5:0,95 limpo vs REF e vs E01–E03.
- Li/Peng: robustez por treino, não por módulo PLM.

---

## 14. Checklist B+C (E04)

- [ ] E03 + val degradado concluídos antes
- [ ] Treino E04 + val limpo + val degradado
- [ ] G3 exportado para slides
- [ ] §4.4 e §5.1 do artigo atualizados

---

## Referências

- [justificativa_yolov11_r.md](justificativa_yolov11_r.md)
- [Plano 03](plano_03_yolov11_treino_padrao.md)
