# Plano Comparativo Futuro (Partes B/C)

## 1) Objetivo comparativo
Comparar diferentes abordagens para reconhecimento de suínos em imagens, avaliando desempenho preditivo e robustez sob diferentes condições de dados.

## 2) Famílias de métodos previstas
- **Clusterização:** K-means e K-medoids (uso exploratório e apoio à compreensão de padrões visuais).
- **Supervisionados clássicos:** SVM, Decision Tree e Random Forest.
- **Detecção:** versões de YOLO (ex.: YOLOv5, YOLOv8, YOLOv11, conforme disponibilidade).

## 3) Variações de particionamento
- Cenário A: 80/20
- Cenário B: 75/25
- Cenário C: 70/30

Observação: fixar `seed` por experimento para reprodutibilidade.

## 4) Cenários de robustez (degradação controlada)
- **Ruído gaussiano:** níveis leve, moderado e alto.
- **Desfoque (blur):** kernel pequeno, médio e grande.
- **Brilho/contraste:** escurecimento e clareamento com variações progressivas.

Objetivo: medir queda de desempenho em relação ao cenário limpo.

## 5) Métricas sugeridas
- **Classificação:** acurácia, precisão, recall, F1.
- **Clusterização:** silhouette score, Davies-Bouldin.
- **Detecção:** mAP, precisão, recall.

## 6) Protocolo de comparação
- Mesmo conjunto-base e mesma política de split por cenário.
- Registrar hiperparâmetros por modelo.
- Reportar média e desvio padrão em repetições controladas.
- Destacar trade-off entre desempenho e custo computacional.

## 7) Resultado esperado
Uma tabela comparativa consolidada por método e cenário, com discussão crítica sobre generalização e sensibilidade a ruídos.
