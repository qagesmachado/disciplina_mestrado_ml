# Entrega Parte B+C — Metodologia e Resultados

Documentação unificada do TCD (EL142A): **50 pts** (B 20 + C 30).

## Início rápido

1. Ler [plano_b_c.md](plano_b_c.md) (cronograma mestre).
2. **Protocolo vigente:** [protocolo_pig_fixo.md](protocolo_pig_fixo.md) — pig/train + pig/val, E01 + E02 + REF.
3. Execução: [../experiments/README.md](../experiments/README.md).
4. Preencher [templates/](templates/) e slides [roteiro_slides_b_c.md](roteiro_slides_b_c.md).

## Dois ambientes Python

| Venv | Modelos | Requirements |
| --- | --- | --- |
| `venv_yolo_5` | E01, REF | `requirements-yolov5.txt` |
| `venv_yolo_ultralytics` | E02 (E03/E04 futuro) | `requirements-ultralytics.txt` |

## Modelos

| ID | Modelo | Plano |
| --- | --- | --- |
| E01 | YOLOv5s | [plano_01](plano_01_yolov5_treino_proprio.md) |
| E02 | YOLOv8s | [plano_02](plano_02_yolov8_treino_padrao.md) |
| E03 | YOLO11s | [plano_03](plano_03_yolov11_treino_padrao.md) |
| E04 | YOLO11-R | [plano_04](plano_04_yolov11_r_robusto.md) |
| REF | `best.pt` | [protocolo_pig_fixo](protocolo_pig_fixo.md) |

## Índice

| Arquivo | Conteúdo |
| --- | --- |
| [plano_b_c.md](plano_b_c.md) | Índice e cronograma B+C |
| [protocolo_pig_fixo.md](protocolo_pig_fixo.md) | **Protocolo vigente** |
| [protocolo_splits_e_experimentos.md](protocolo_splits_e_experimentos.md) | Legado S1–S3 (obsoleto) |
| [analise_desempenho_baseline.md](analise_desempenho_baseline.md) | Saturação mAP, H1 |
| [secao_metodologia_artigo.md](secao_metodologia_artigo.md) | §3 artigo |
| [secao_resultados_discussao_artigo.md](secao_resultados_discussao_artigo.md) | §4–5 artigo |
| [checklist_rubrica_b_c.md](checklist_rubrica_b_c.md) | Rubrica B+C |

## Artigo

- [Etapa 1](../TCD/entrega%20parcial%201/Etapa1_GustavoMachado.doc)
- [rascunho etapa 2](../TCD/rascunho_artigo_etapa2.md)
