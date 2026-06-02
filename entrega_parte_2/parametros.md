# Hiperparâmetros dos experimentos

Referência dos valores em `experiments/YOLO_V5/config/experiments_yolov5.yaml` (bloco `defaults`). Os experimentos E02 (YOLOv8) e E03 (YOLO11) usam a mesma estrutura em `experiments/YOLO_V8/config/experiments.yaml` e `experiments/YOLO_V11/config/experiments.yaml`.

## Valores padrão (E01 — YOLOv5)

```yaml
defaults:
  imgsz: 640
  epochs: 100
  batch: 16
  patience: 20
  seed: 42
  conf_thres: 0.25
  workers: 4
  device: auto
  batch_cpu: 8
```

Esses são os **hiperparâmetros padrão** do experimento. A maioria entra no **treino**; alguns também afetam a **validação**. Todos podem ser sobrescritos na linha de comando (ex.: `--epochs 2`, `--batch 8`).

## Onde entra cada parâmetro

| Parâmetro | Treino | Validação |
| --- | --- | --- |
| `imgsz` | ✅ | ✅ |
| `epochs` | ✅ | — |
| `batch` | ✅ | ✅ |
| `patience` | ✅ | — |
| `seed` | ✅ | — |
| `conf_thres` | — | ✅ |
| `workers` | ✅ | — |
| `device` | ✅ | ✅ |
| `batch_cpu` | ✅ (fallback CPU) | ✅ (fallback CPU) |

Scripts que leem esses valores: `treinar_yolov5.py`, `validar_yolov5.py` (e equivalentes em YOLO_V8/YOLO_V11).

---

## Descrição de cada parâmetro

### `imgsz: 640`

Tamanho (px) para redimensionar as imagens no treino e na validação.

- **Aumentar** (ex.: 1280): objetos pequenos ficam mais fáceis de detectar; treino mais lento e consome mais VRAM.
- **Diminuir** (ex.: 416): mais rápido e leve; pode perder precisão em detalhes finos.
- 640 é o padrão do YOLOv5 no COCO.

### `epochs: 100`

Quantas vezes o modelo passa pelo dataset de treino.

- **Aumentar**: mais tempo de aprendizado; risco de overfitting se passar do ideal.
- **Diminuir**: treino mais rápido; o modelo pode não convergir bem.
- Para teste rápido, use `--epochs 2` no script sem mudar o YAML.

### `batch: 16`

Quantas imagens processadas por passo de gradiente (GPU).

- **Aumentar**: treino mais estável e rápido por época, se couber na VRAM; se não couber → erro de memória (OOM).
- **Diminuir**: usa menos memória; gradiente mais ruidoso; treino pode ficar mais lento.
- Na CPU, o projeto limita automaticamente a `batch_cpu` (8).

### `patience: 20`

Early stopping: se a métrica de validação não melhorar por N épocas, o treino para antes.

- **Aumentar**: espera mais antes de parar; treino mais longo; pode ajudar se a curva oscila.
- **Diminuir**: para mais cedo; risco de parar antes do modelo convergir.
- O melhor checkpoint (`best.pt`) é o da época com melhor validação, não necessariamente a última.

### `seed: 42`

Semente aleatória (shuffle, augmentations, inicialização).

- **Mudar**: resultados ligeiramente diferentes a cada run.
- **Fixar** (42): ajuda a reproduzir o mesmo experimento no mesmo hardware/software.

### `conf_thres: 0.25`

Limiar de confiança — usado só na **validação/inferência**, não no treino.

- Detecções com score abaixo disso são descartadas.
- **Aumentar** (ex.: 0.5): menos detecções, mais precisão, menos recall (pode perder objetos).
- **Diminuir** (ex.: 0.1): mais detecções, mais recall, mais falsos positivos.
- 0.25 é o padrão do YOLO.

### `workers: 4`

Threads para carregar imagens em paralelo durante o treino (DataLoader).

- **Aumentar**: pode acelerar o treino se o disco/CPU aguentar.
- **Diminuir**: menos carga no sistema; pode deixar a GPU ociosa.
- No Windows/CPU, o projeto força `workers=0` (evita problemas de multiprocessing).

### `device: auto`

Onde roda treino e validação.

- `auto`: GPU (`0`) se CUDA existir; senão CPU.
- `0` ou `cuda`: força GPU.
- `cpu`: força CPU (bem mais lento).
- Se pedir GPU sem CUDA, cai para CPU com aviso.

### `batch_cpu: 8`

Teto de batch quando roda em CPU.

- Se `batch: 16` e `device` resolver para CPU, o batch efetivo vira **8**.
- **Aumentar**: treino CPU um pouco mais rápido por época, mas mais RAM; pode travar a máquina.
- **Diminuir**: mais seguro em máquinas fracas; treino mais lento.

---

## Parâmetros fora do bloco `defaults`

No mesmo YAML, mas específicos do experimento E01:

| Campo | Valor | Função |
| --- | --- | --- |
| `weights_init` | `yolov5s.pt` | Pesos iniciais (backbone pré-treinado no COCO) |
| `model_label` | `YOLOv5s_autoral` | Nome exibido nos relatórios |
| `run_name` | `E01_yolov5s_pig` | Pasta de saída em `outputs/E01_yolov5s_pig/` |

Alternativa mais leve: trocar `weights_init` para `yolov5n.pt` e ajustar `run_name` (ex.: `E01_yolov5n_pig`).

---

## Regra prática

- **Treino:** mexa primeiro em `epochs`, `batch` e `device`.
- **Métricas de validação** (precision, recall, F1): `conf_thres` é o que mais impacta.
- **Comparação justa** entre E01, E02 e E03: mantenha `seed`, `imgsz` e `conf_thres` iguais entre runs.
