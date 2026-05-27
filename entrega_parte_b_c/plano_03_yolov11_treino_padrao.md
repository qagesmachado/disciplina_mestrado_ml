# Plano 03 — YOLO11s: treino autoral padrão (Ultralytics)

> **Execução futura:** mesmo padrão do [Plano 02](plano_02_yolov8_treino_padrao.md) — dataset **pig fixo**, `venv_yolo_ultralytics`, `treinar_ultralytics.py` / `validar_ultralytics.py`. Splits S1–S3 abaixo são legado.

Detector **YOLO11s** com pipeline **default** Ultralytics — geração mais recente e estável no ecossistema [ultralytics](https://github.com/ultralytics/ultralytics), para comparar evolução **v5 → v8 → v11** sem adaptações de robustez.

**Matriz:** E03 (S1), E09 (S2), E10 (S3) — ver [protocolo](protocolo_splits_e_experimentos.md).

---

## 1. Objetivo e hipótese

**Objetivo:** treinar YOLO11s no dataset `pig` com augmentação padrão, paridade de hiperparâmetros com E01 e E02.

**Hipótese (H2b):** no split S1, E03 apresenta mAP@0,50 e/ou mAP@0,50:0,95 **≥** E02 (YOLOv8s), refletindo ganho de arquitetura mais recente.

---

## 2. Pré-requisitos

| Item | Detalhe |
| --- | --- |
| Ambiente | `venv_yolo_5` ou venv com `ultralytics` atualizado |
| Pacote | `pip install -U ultralytics` |
| Pesos iniciais | `yolo11s.pt` (download automático) |
| Dados | YAMLs em `data/yaml/data_split_*.yaml` |

**Verificação:**

```powershell
python -c "from ultralytics import YOLO; YOLO('yolo11s.pt'); print('OK')"
```

---

## 3. Dados

| Experimento | YAML | Train / Val |
| --- | --- | --- |
| E03 | `data/yaml/data_split_80_20.yaml` | 852 / 213 |
| E09 | `data/yaml/data_split_75_25.yaml` | 799 / 266 |
| E10 | `data/yaml/data_split_70_30.yaml` | 746 / 319 |

---

## 4. Configuração de treino

| Parâmetro | Valor |
| --- | --- |
| `model` | `yolo11s.pt` |
| `imgsz` | 640 |
| `epochs` | 100 |
| `batch` | 16 ou 8 |
| `patience` | 20 |
| `seed` | 42 |
| Augmentação | **default Ultralytics** |
| `project` | `outputs/experiments` |
| `name` | `E03_yolo11s_80_20` |

**Diff vs Plano 04:** sem copy-paste reforçado, blur/ruído no treino ou HSV elevado.

---

## 5. Comandos previstos (execução futura)

### E03 — treino S1

```powershell
yolo detect train ^
  model=yolo11s.pt ^
  data=data/yaml/data_split_80_20.yaml ^
  imgsz=640 ^
  epochs=100 ^
  batch=16 ^
  patience=20 ^
  seed=42 ^
  project=outputs/experiments ^
  name=E03_yolo11s_80_20 ^
  exist_ok=True
```

### E09, E10 — Fase 2

- `E09_yolo11s_75_25` com `data_split_75_25.yaml`
- `E10_yolo11s_70_30` com `data_split_70_30.yaml`

---

## 6. Validação

```powershell
yolo detect val ^
  model=outputs/experiments/E03_yolo11s_80_20/weights/best.pt ^
  data=data/yaml/data_split_80_20.yaml ^
  imgsz=640 ^
  conf=0.25
```

Exportar P, R, mAP50, mAP50-95 para tabela consolidada.

---

## 7. Saídas esperadas

`outputs/experiments/E03_yolo11s_80_20/weights/best.pt` + `results.csv` + relatório de val.

---

## 8. Comparação

| Par | Foco |
| --- | --- |
| E03 vs E02 | v11 vs v8 |
| E03 vs E01 | v11 vs v5 |
| E03 vs E04 | Isolar efeito do protocolo robusto (Plano 04) |
| vs REF | Baseline externo S1 |

---

## 9. Critérios de sucesso

- Métricas registradas no mesmo protocolo que E01/E02
- Curvas de treino arquivadas para gráficos do artigo

---

## 10. Checklist pós-treino

- [ ] E02 concluído antes (comparação v8 vs v11)
- [ ] `args.yaml` salvo
- [ ] Linha na tabela Fase 1 (E01–E04)

---

## 11. Validação val degradado

**Obrigatório para H3:** após val limpo, executar val nas imagens degradadas (mesmo split):

| Cenário | Transformação |
| --- | --- |
| `brilho_escuro` | fator 0,7 |
| `brilho_claro` | fator 1,3 |
| `blur` | Gaussian blur moderado |
| `ruido` | σ leve |

Script previsto: `scripts/gerar_val_degradado.py` + `validar_detector.py`.

Registrar em `templates/tabela_robustez.csv` linhas E03.

---

## 12. Tabelas e gráficos

| Artefato | Destino |
| --- | --- |
| E03 S1 | `templates/tabela_resultados_s1.csv` |
| E09, E10 | `templates/tabela_splits.csv` |
| Robustez | `templates/tabela_robustez.csv` |
| G3 | Queda relativa vs E04 |

---

## 13. Parágrafo de discussão

- **H2b:** E03 vs E02.
- **H3:** baseline para E04 no val degradado.
- Cenas densas: comentar Recall e erro de contagem.

---

## 14. Checklist B+C (E03)

- [ ] Treino E03
- [ ] Val limpo + **val degradado completo**
- [ ] tabela_robustez E03 preenchida
- [ ] Comparar com E04 antes do slide 13

---

## Referências

- [Plano 02 — YOLOv8s](plano_02_yolov8_treino_padrao.md)
- [Plano 04 — YOLO11-R](plano_04_yolov11_r_robusto.md)
- [Ultralytics YOLO11](https://docs.ultralytics.com/models/yolo11/)
