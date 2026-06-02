# Algoritmos selecionados — YOLOv5s, YOLOv8s, YOLO11s

Três detectores de objetos (Aprendizado de Máquina **supervisionado**), treinados pelo autor no Kaggle Pig Dataset. Pesos iniciais COCO; checkpoints finais próprios.

---

## Tabela comparativa (síntese)

| Aspecto | YOLOv5s (E01) | YOLOv8s (E02) | YOLO11s (E03) |
| --- | --- | --- | --- |
| Nome completo | You Only Look Once v5 small | YOLOv8 small | YOLO11 small |
| Categoria | Detecção supervisionada (single-stage) | Idem | Idem |
| Ecossistema | pacote `yolov5` | [Ultralytics](https://docs.ultralytics.com/pt/quickstart) | Ultralytics |
| Detecção | anchor-based | anchor-free | anchor-free (evolução do v8) |
| Pesos iniciais | `yolov5s.pt` | `yolov8s.pt` | `yolo11s.pt` |
| Venv | `venv_yolo_5` | `venv_yolo_ultralytics` | mesmo venv do E02 |
| Papel no TCD | baseline da literatura em suínos | geração intermediária | geração atual |

---

## 1. YOLOv5s (E01)

**Objetivo no problema:** estabelecer baseline reprodutível alinhada à literatura de detecção de suínos [Li and Li 2024; Peng et al. 2024] e à Etapa 1 do TCD.

**Vantagens:** amplo uso em suinocultura; repositório maduro; bom desempenho em cenas densas após fine-tuning.

**Limitações:** arquitetura anchor-based (mais parâmetros de ancora); pipeline separado do ecossistema Ultralytics; inferência mais lenta que v8/v11 no mesmo hardware.

**Justificativa:** referência histórica e científica do domínio; permite comparar se gerações mais novas superam o v5 no mesmo protocolo.

**Hiperparâmetros:** `imgsz=640`, `epochs=100`, `patience=20`, `seed=42`, augmentação padrão YOLOv5.

---

## 2. YOLOv8s (E02)

**Objetivo no problema:** avaliar a geração intermediária Ultralytics (anchor-free, cabeça e perdas redesenhadas) no mesmo domínio de leitões.

**Vantagens:** API unificada (`from ultralytics import YOLO`); treino e validação simplificados; inferência ~2,8–3× mais rápida que v5 nos testes locais (131,9 vs 372,1 ms/img).

**Limitações:** resultados preliminares abaixo do E01 em mAP@0.50:0.95; depende de configuração correta de PyTorch/GPU no Windows.

**Justificativa:** ponto intermediário na evolução YOLO; isolado do v5 por usar venv e framework distintos, garantindo comparação justa de gerações.

**Hiperparâmetros:** mesmos de E01; augmentação padrão Ultralytics.

Treino mínimo (reprodutibilidade):

```python
from ultralytics import YOLO
model = YOLO("yolov8s.pt")
model.train(data="pig_dataset.yaml", epochs=100, imgsz=640, patience=20, seed=42)
```

---

## 3. YOLO11s (E03)

**Objetivo no problema:** testar a geração mais recente estável do ecossistema Ultralytics sobre o mesmo conjunto fixo.

**Vantagens:** evolução arquitetural sobre v8; mesmo venv e pipeline do E02 (só muda o arquivo de pesos); mAP@0.50:0.95 ligeiramente superior ao E02 nos resultados preliminares (0,8025 vs 0,7986).

**Limitações:** ganhos modestos frente ao v5 em métricas rigorosas; literatura específica em suínos ainda concentrada em v5.

**Justificativa:** verificar se a geração atual justifica migração em relação ao baseline v5, mantendo protocolo idêntico.

**Hiperparâmetros:** idênticos ao E02; pesos iniciais `yolo11s.pt`.

---

## Evolução arquitetural (comparação conceitual)

| Tema | YOLOv5 | YOLOv8 / YOLO11 |
| --- | --- | --- |
| Caixas | anchors pré-definidos | predição direta (anchor-free) |
| Backbone | CSPDarknet | C2f e blocos otimizados (v11 refina v8) |
| Treino | CLI/repo yolov5 | `model.train()` Ultralytics |
| CLI alternativa | `python train.py` | `yolo detect train model=... data=...` |

Referência oficial: [Instalação Ultralytics](https://docs.ultralytics.com/pt/quickstart).

---

## Referências

- L. Li and F. Li, "Pig Detection Method Based on Improved YOLOv5," ISDH 2024.
- N. Peng, F. Li and X. Luo, "PLM-YOLOv5: Improved YOLOv5 for Pig Detection in Livestock Monitoring," IRAC 2024.
- ULTRALYTICS. YOLOv5. GitHub, 2022. https://github.com/ultralytics/yolov5
- ULTRALYTICS. Documentação Ultralytics. https://docs.ultralytics.com/pt/quickstart

**Nota:** o modelo `best.pt` do dataset (Etapa 1) não entra como um dos três algoritmos desta entrega — foi apenas baseline exploratório inicial (P=0,650; mAP@0,50=0,785).
