# Checklist — Rubrica B+C (50 pts)

---

## B — Metodologia e Desenho da Pesquisa (20 pts)

### Fluxograma (Graphical Abstract)


| Critério                                                        | Status | Evidência                              |
| --------------------------------------------------------------- | ------ | -------------------------------------- |
| Fluxo dados → treino → avaliação → tabelas/gráficos → discussão | [ ]    | [fluxograma_b_c.md](fluxograma_b_c.md) |
| REF externo distinguido                                         | [ ]    | Slides 2, 4                            |
| Partição pig fixo (train/val Kaggle)                            | [ ]    | [protocolo_pig_fixo.md](protocolo_pig_fixo.md) |
| E02 com venv_yolo_ultralytics isolada                           | [ ]    | [plano_02](plano_02_yolov8_treino_padrao.md) |


### Algoritmos (mín. 3; entregue 4)


| #   | Algoritmo | OK  | Documento                          |
| --- | --------- | --- | ---------------------------------- |
| 1   | YOLOv5s   | [ ] | plano_01                           |
| 2   | YOLOv8s   | [ ] | plano_02                           |
| 3   | YOLO11s   | [ ] | plano_03                           |
| 4   | YOLO11-R  | [ ] | plano_04 + justificativa_yolov11_r |



| Critério                                                   | Status |
| ---------------------------------------------------------- | ------ |
| Justificativa de cada papel                                | [ ]    |
| Método adicional no YOLO11-R explícito                     | [ ]    |
| [secao_metodologia_artigo.md](secao_metodologia_artigo.md) | [ ]    |


---

## C — Resultados e Discussão (30 pts)

### Tabelas e gráficos comparativos


| Critério                              | Status | Evidência                                     |
| ------------------------------------- | ------ | --------------------------------------------- |
| Tabela comparativa S1 (E01–E04 + REF) | [ ]    | templates/tabela_resultados_s1.csv + Slide 11 |
| Gráfico barras ou equivalente         | [ ]    | G1 — graficos_especificacao.md                |
| Gráfico robustez E03 vs E04           | [ ]    | G3 + tabela_robustez.csv                      |
| Gráfico splits (opcional completo)    | [ ]    | G2 + tabela_splits.csv                        |


### Discussão crítica com métricas adequadas


| Critério                                                                     | Status |
| ---------------------------------------------------------------------------- | ------ |
| Discussão usa P, R, mAP@0,5, mAP@0,5:0,95                                    | [ ]    |
| Val degradado comentado (H3)                                                 | [ ]    |
| Não usa acurácia/silhueta/R² como principal                                  | [ ]    |
| [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md) | [ ]    |
| Slides 15–16 (discussão + literatura)                                        | [ ]    |


### Ligação Etapa 1


| Critério                           | Status |
| ---------------------------------- | ------ |
| Mesmo dataset e problema           | [ ]    |
| REF com métricas Etapa 1 na tabela | [ ]    |


---

## Entregáveis da pasta


| Arquivo                              | OK  |
| ------------------------------------ | --- |
| plano_b_c.md                         | [ ] |
| protocolo_pig_fixo.md                | [ ] |
| protocolo_splits_e_experimentos.md (legado) | [ ] |
| planos 01–04 (com §11–14)            | [ ] |
| templates/*                          | [ ] |
| fluxograma_b_c.md                    | [ ] |
| roteiro_slides_b_c.md                | [ ] |
| secao_metodologia_artigo.md          | [ ] |
| secao_resultados_discussao_artigo.md | [ ] |
| README.md                            | [ ] |


---

## Conclusão

- Rubrica B coberta  
- Rubrica C coberta (mínimo: tabela S1 + G1 + discussão; completo: + splits + G3)

