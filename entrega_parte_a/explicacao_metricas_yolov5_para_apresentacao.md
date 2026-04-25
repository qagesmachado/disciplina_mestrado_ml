# Explicação das métricas YOLOv5 (para slides)

## Métricas principais

- **Precisão (Precision)**  
  Entre todas as detecções feitas pelo modelo, qual fração estava correta.  
  Fórmula: `TP / (TP + FP)`.

- **Revocação (Recall)**  
  Entre todos os porcos reais anotados no conjunto, qual fração foi detectada.  
  Fórmula: `TP / (TP + FN)`.

- **mAP@0.50**  
  Média da precisão por classe, considerando IoU >= 0.50.
  Interpreta se o modelo encontra e posiciona caixas de forma razoável.

- **mAP@0.50:0.95**  
  Média do AP em múltiplos limiares de IoU (0.50 a 0.95, passo 0.05).
  É um indicador mais rigoroso da qualidade fina do ajuste das caixas.

## Como interpretar os resultados atuais

- `Precisão` moderada + `Recall` alto: o modelo encontra a maioria dos porcos, mas ainda cria algumas caixas extras.
- `mAP@0.50` maior que `mAP@0.50:0.95`: a detecção de presença é boa, porém o ajuste exato das bounding boxes ainda pode melhorar.

## Texto curto para usar no slide

"O modelo apresentou boa capacidade de detecção de suínos no conjunto de validação, com alta cobertura dos alvos (Recall), porém com margem para redução de falsos positivos (Precision) e para refinamento do posicionamento das caixas, evidenciado pela diferença entre mAP@0.50 e mAP@0.50:0.95."
