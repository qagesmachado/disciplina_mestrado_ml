# Reconhecimento de Leitões em Imagens: Definição do Problema, Caracterização da Base e Análise Exploratória Inicial

## Abstract
This study presents an investigation into piglet recognition in images, defining the problem, characterizing the database, and conducting an exploratory analysis. The database used contains annotations in YOLO format organized into training and validation partitions. Statistical analysis indicated a high density of instances per image and low variability in density between images or relevant factors such as partial occlusion. As a reference, a pre-trained YOLOv5 model was used, obtaining Precision = 0.650355, Recall = 0.854322, mAP@0.50 = 0.784785, and mAP@0.50:0.95 = 0.273314 in the validation set. Based on these results, a comparative protocol will be proposed for subsequent steps.

## Resumo
Este estudo apresenta uma investigação sobre o reconhecimento de leitões em imagens, com definição do problema, caracterização da base de dados e análise exploratória. A base utilizada contém anotações no formato YOLO organizada em partições de treino e validação. A análise estatística indicou alta densidade de instâncias por imagem e baixa variabilidade de densidade entre as imagens ou fatores relevantes como oclusão parcial. Como referência, um modelo YOLOv5 pré-treinado, obtendo-se Precision = 0,650355, Recall = 0,854322, mAP@0,50 = 0,784785 e mAP@0,50:0,95 = 0,273314 no conjunto de validação. Com base nesses resultados, será proposto um protocolo comparativo para etapas subsequentes.

## 1. Introdução
A detecção de objetos em imagens e vídeos é um tema central em Visão Computacional, com aplicações em monitoramento inteligente e automação de processos. No domínio de suinocultura de precisão, abordagens recentes baseadas em YOLOv5 têm apresentado resultados promissores para detecção de suínos em ambientes de produção, incluindo variações arquiteturais voltadas à melhoria de robustez e acurácia [Li and Li 2024; Peng et al. 2024]. Neste trabalho, adota-se YOLOv5 como referência técnica de implementação e comparação [Ultralytics 2022].

No domínio de monitoramento animal, a detecção automática de leitões em ambiente coletivo apresenta desafios práticos, como alta concentração de indivíduos por quadro, sobreposição entre os corpos e variações de iluminação. Nesses cenários, a etapa de caracterização dos dados é determinante para o desenho experimental e para a interpretação correta de métricas de desempenho.

Do ponto de vista metodológico, este trabalho adota uma estratégia incremental de investigação, com diagnóstico inicial de dados e definição explícita de métricas antes da etapa de comparação de modelo. Diante desse contexto, o presente texto consolida a fase inicial da investigação, estabelecendo a questão de pesquisa, descrevendo a base utilizada, apresentando resultados exploratórios e registrando um baseline de referência para comparações futuras.


## 2. Análise exploratória da base de dados
Nesta etapa, foi utilizado o conjunto de dados de leitões, obtido no Kaggle Pig Dataset [ZIMANGE, s. d.], com anotações no padrão YOLO e organização em partições de treino e validação.

Na caracterização inicial da base, observou-se uma separação 929 imagens para treino (Figura 1), correspondendo 80% da base de dados, e 136 imagens para validação (Figura 2), representando os 20% restante da base de dados.

Complementarmente à contagem de instâncias, foi conduzida uma verificação orientada à consistência espacial das anotações. Para tanto, desenvolveu-se um script em Python que lê os arquivos de rótulo no formato YOLO, converte as coordenadas normalizadas para o plano da imagem em pixels e sobrepõe retângulos delimitadores às imagens correspondentes. Esse procedimento viabiliza a inspeção manual de amostras, permitindo detectar desalinhamentos entre rótulo e conteúdo visual, erros de classe ou inconsistências de escala antes de etapas de treinamento e avaliação, Figura 3.

Adicionalmente, analisou-se a distribuição do número de leitões por imagem a partir do **gabarito** anotado (rótulos YOLO) nas partições de treino e validação, **sem utilização de modelo de detecção** (Tabela 1). A faixa de contagem por quadro apresenta **baixa amplitude**: no treino, entre **11 e 15** instâncias por imagem; na validação, entre **12 e 15** (não há, na validação, imagens com exatamente 11 leitões). A massa da distribuição **concentra-se em *k* = 13 e, em especial, em *k* = 14**; em ambas as partições, a moda ocorre em 14 leitões por imagem, o que indica **alta homogeneidade** na carga de objetos por cena nesse recorte e antecipa desafios de detecção em cenas com **alta densidade** de alvos.

## 3. Metodologia
O procedimento metodológico foi estruturado em três etapas complementares. Primeiramente, realizou-se o levantamento e a organização da base anotada em formato YOLO, com verificação da consistência das partições de treino e validação. Em seguida, executaram-se rotinas de análise exploratória para quantificar a distribuição de objetos por imagem e produzir visualizações de apoio. Por fim, empregou-se uma avaliação de referência com YOLOv5 pré-treinado (`best.pt`), com o objetivo de estabelecer um ponto inicial de comparação entre abordagens.

A avaliação adotou métricas padronizadas de detecção de objetos (Precision, Recall, mAP@0,50 e mAP@0,50:0,95), complementadas por análise por imagem com indicadores de acerto e erro (TP, FP e FN). A implementação foi conduzida por scripts reprodutíveis, com geração de artefatos em CSV e HTML, assegurando rastreabilidade e documentação dos resultados obtidos.

## 4. Próximos passos
Os próximos passos do estudo concentram-se na comparação sistemática de modelos e configurações, com ênfase em desempenho e robustez no cenário de detecção de leitões.

Nesse contexto, as ações planejadas são:
1. Treinar modelo próprio no mesmo dataset, mantendo rastreabilidade dos experimentos.
2. Comparar variantes do YOLOv5 e possíveis adaptações descritas na literatura para detecção de suínos [Li and Li 2024; Peng et al. 2024].
3. Avaliar sensibilidade a parâmetros de inferência (`conf_thres`, `imgsz` e `batch`).
4. Investigar robustez sob degradações controladas (ruído, blur e variação de iluminação).
5. Consolidar análise conjunta de métricas globais e diagnóstico por imagem.

Na versão consolidada do trabalho, será incluída uma tabela comparativa de experimentos com critérios uniformes de avaliação, favorecendo a análise de trade-offs entre diferentes estratégias.

## 5. Considerações finais
A etapa inicial permitiu consolidar a compreensão da base, estruturar a análise exploratória e definir uma metodologia reprodutível para avaliação de detectores no domínio da suinocultura de precisão. Assim, o estudo avança para uma fase de comparação orientada por métricas e evidências experimentais, em alinhamento com os objetivos das próximas etapas da investigação.

## Referências
- Li, L.; Li, F. Pig Detection Method Based on Improved YOLOv5. In: 2024 International Symposium on Digital Home (ISDH), Guilin, China, 2024. p. 91-96. DOI: 10.1109/ISDH64927.2024.00022.
- Peng, N.; Li, F.; Luo, X. PLM-YOLOv5: Improved YOLOv5 for Pig Detection in Livestock Monitoring. In: 2024 International Conference on Intelligent Robotics and Automatic Control (IRAC), Guangzhou, China, 2024. p. 619-625. DOI: 10.1109/IRAC63143.2024.10871878.
- ULTRALYTICS. YOLOv5. GitHub, [S. l.], 2022. Disponível em: https://github.com/ultralytics/yolov5. Acesso em: 24 abr. 2026.
- ZIMANGE. Pig Dataset. Kaggle, [S. l.], [s. d.]. Disponível em: https://www.kaggle.com/datasets/zimange/pig-dataset. Acesso em: 24 abr. 2026.

