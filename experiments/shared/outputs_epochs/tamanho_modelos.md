# Tamanho dos modelos — best.pt (média entre todas as épocas)

Média do `best.pt` por arquitetura (soma dos 10 best.pt — épocas 1, 2, 3, 4, 5, 10, 15, 20, 25, 50 — dividida por 10).


| Modelo  | Parâmetros | GFLOPs | Tamanho médio (bytes) | Tamanho médio (MiB) |
| ------- | ---------- | ------ | --------------------- | ------------------- |
| YOLOv5s | 7.022.326  | 15,9   | 14.442.863            | 13,774              |
| YOLOv8s | 11.135.987 | 28,6   | 22.513.834            | 21,471              |
| YOLO11s | 9.428.179  | 21,5   | 19.172.455            | 18,284              |


Parâmetros e GFLOPs são fixos pela arquitetura (não mudam entre épocas; dependem só do nº de classes = 1). Extraídos dos `best.pt`: v8/v11 via `YOLO(best.pt).model.info()`; v5 via `ckpt['model'].info()` (640px).

## Variação percentual entre médias


| Comparação        | Origem (MiB) | Destino (MiB) | Variação |
| ----------------- | ------------ | ------------- | -------- |
| YOLOv5s → YOLOv8s | 13,774       | 21,471        | +55,88%  |
| YOLOv8s → YOLO11s | 21,471       | 18,284        | -14,84%  |
| YOLOv5s → YOLO11s | 13,774       | 18,284        | +32,75%  |


Leitura: o YOLOv8s é o maior (+55,88% sobre o YOLOv5s). O YOLO11s reduz parte disso (14,84% menor que o YOLOv8s), mas ainda fica 32,75% acima do YOLOv5s.