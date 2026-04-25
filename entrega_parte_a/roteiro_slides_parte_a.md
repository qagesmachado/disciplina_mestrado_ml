# Roteiro de Slides - Parte A (TCD)

## Slide 1 - Título e enquadramento
- **Título sugerido:** Definição do Problema e Exploração Inicial de Dados para Reconhecimento de Suínos em Imagens
- Disciplina: EL142A - Aprendizado de Máquinas
- Contexto: trabalho da disciplina conectado ao tema de visão computacional do mestrado
- Delimitação: foco exclusivo na Parte A (problema + EDA), sem executar o escopo completo da tese

## Slide 2 - Questão central de pesquisa
**Pergunta central (usar em destaque):**

Como caracterizar e preparar um conjunto de imagens anotadas de suínos para sustentar, nas próximas etapas, a comparação entre métodos de clusterização, aprendizado supervisionado e modelos de detecção?

## Slide 3 - Motivação e justificativa
- Relevância prática: monitoramento de suínos por visão computacional pode apoiar automação e acompanhamento no ambiente produtivo.
- Relevância científica: fornece base experimental para comparar diferentes famílias de métodos de ML.
- Justificativa didática: a Parte A estabelece qualidade e entendimento dos dados antes da modelagem.

## Slide 4 - Relação com o mestrado (contextual)
- Conexão direta com a linha de pesquisa: visão computacional aplicada a suínos.
- Este TCD aproveita o mesmo domínio de aplicação, mas em recorte metodológico de disciplina.
- O plano de pesquisa de mestrado serve como contexto, não como escopo de implementação nesta entrega.

## Slide 5 - Base de dados selecionada
- Dataset: `pig` (fonte Kaggle documentada em `pig/kaggle_dataset_link.txt`).
- Estrutura de anotações: formato YOLO (arquivos `.txt` por imagem).
- Splits encontrados localmente: `train` e `val`.
- Classe anotada no conjunto atual: classe `0` (suíno).

## Slide 6 - Estatísticas gerais da base
Usar os resultados de `outputs/parte_a_eda/summary.json`:

- Total de imagens: **1065**
- Treino: **929** | Validação: **136**
- Total de bounding boxes: **14798**
- Resolução das imagens: min **640x640**, max **1080x1080**, média aproximada **860x860**
- Densidade de boxes por imagem: min **11**, max **15**, média **13.895**

Inserir figura: `outputs/parte_a_eda/01_imagens_por_split.png`

## Slide 7 - Exploração visual e distribuição dos dados
Inserir e comentar:
- `outputs/parte_a_eda/02_dispersao_resolucoes.png`
- `outputs/parte_a_eda/03_boxes_por_imagem.png`
- `outputs/parte_a_eda/04_largura_bbox.png`
- `outputs/parte_a_eda/05_altura_bbox.png`
- `outputs/parte_a_eda/07_area_bbox.png`

Mensagem principal:
- O conjunto apresenta padrão consistente de resolução e alta densidade de objetos por imagem.
- As distribuições de tamanho de box ajudam a antecipar desafios de detecção em objetos pequenos/medianos.

## Slide 8 - Inspeção qualitativa com imagens anotadas
Inserir: `outputs/parte_a_eda/06_amostras_anotadas.png`

Pontos de fala:
- Conferência visual da qualidade das anotações.
- Verificação de cenas com múltiplos suínos por frame.
- Identificação preliminar de possíveis variações de cenário e iluminação.

## Slide 9 - Fechamento da Parte A
- A questão de pesquisa foi definida.
- Motivação, contexto acadêmico e relação com o mestrado foram estabelecidos.
- A base foi descrita e analisada com evidências numéricas e visuais.
- Resultado: conjunto apto para avançar para desenho metodológico (Parte B).

## Slide 10 - Ponte para comparação futura (sem executar agora)
- Métodos clássicos previstos: K-means, K-medoids, SVM, Decision Tree, Random Forest.
- Métodos de detecção previstos: comparação entre versões de YOLO.
- Estratégias de split para comparação futura: 80/20, 75/25 e 70/30.
- Robustez futura: cenários com ruído, blur e variação de brilho para testar sensibilidade.

## Checklist da rubrica A (para conferência final)
- Questão central apresentada
- Motivação e justificativa apresentadas
- Relação com pesquisa de mestrado explicada
- Base de dados descrita (origem, estrutura e volume)
- Visualização analítica inicial incluída com gráficos e inspeção qualitativa
