# Análise de desempenho — E01 vs REF (pig/val)

Base: `experiments/shared/outputs/comparacao_pig_baseline.md`.

## Resultado E01 vs REF

| Métrica | E01 | REF |
| --- | ---: | ---: |
| mAP@0,50 | 0,9914 | 0,9924 |
| mAP@0,50:0,95 | 0,8302 | 0,8301 |
| Recall | 0,9776 | 0,9851 |

**Conclusão H1:** equivalência em mAP@0,50 (saturação ~99%); REF ligeiramente melhor em Recall.

## Implicação para E02 (H2a)

Com o benchmark saturado para YOLOv5s, ganhos de E02 (YOLOv8) devem ser avaliados em **mAP@0,50:0,95** e Recall, não só mAP@0,50.
