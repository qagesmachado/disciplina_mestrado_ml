# Seção 4 — Resultados e Discussão (texto para o artigo)

Complementa [secao_metodologia_artigo.md](secao_metodologia_artigo.md). Preencher após execução dos experimentos; usar [templates/](templates/).

---

## 4. Resultados

### 4.1 Desempenho no conjunto de validação fixo (`pig/val`, 136 imagens)

A Tabela X consolida Precision (P), Recall (R), mAP@0,50 e mAP@0,50:0,95 no **mesmo** `pig/val` para E01, E02 (quando disponível), E03–E04 e REF.

| Exp. | Modelo | P | R | mAP@0,50 | mAP@0,50:0,95 |
| --- | --- | --- | --- | --- | --- |
| E01 | YOLOv5s | 0,992 | 0,978 | 0,991 | 0,830 |
| E02 | YOLOv8s | _após treino_ | | | |
| E03 | YOLO11s | | | | |
| E04 | YOLO11-R | | | | |
| REF | best.pt (terceiros) | 0,650 | 0,854 | 0,785 | 0,273 |

_Fonte de dados: [templates/tabela_resultados_s1.csv](templates/tabela_resultados_s1.csv)._

**Figura X — Gráfico de barras:** mAP@0,50 por modelo (E01–E04 e REF). Ver [templates/graficos_especificacao.md](templates/graficos_especificacao.md) (G1).

**H1 (E01 vs REF):** no `pig/val`, mAP@0,50 ~0,99 em ambos — **saturação** do benchmark; diferença principal em Recall (REF ligeiramente superior). H1 não se confirma com margem forte em mAP@0,50.

**H2a (E02 vs E01):** _preencher após `YOLO_V8/run_yolov8_pig.ps1`._

Interpretação esperada:
- Comparar progressão **v5 → v8 → v11** (H2a, H2b) no mesmo val.
- Contrastar modelos autorais com REF (H1) sem tratar REF como resultado do autor.

### 4.2 Curvas de treino

Incluir figuras de evolução de loss e mAP na validação para E01–E04 (ex.: `results.png` de cada run). Comentar convergência e early stopping (`patience = 20`).

### 4.3 Sensibilidade ao particionamento treino/validação

A Tabela Y apresenta as métricas principais nos cenários S1 (80/20), S2 (75/25) e S3 (70/30) para cada família de modelo (E01/E05/E06, etc.).

_Fonte: [templates/tabela_splits.csv](templates/tabela_splits.csv)._

**Figura Y — Linhas:** Recall ou mAP@0,50 em função da fração de treino (H4).

### 4.4 Robustez sob validação degradada

Comparou-se YOLO11s (E03) e YOLO11-R (E04) em validação **limpa** e **degradada** (variações de brilho, desfoque e ruído), calculando a queda relativa:

\[
\Delta = \frac{M_{\mathrm{limpo}} - M_{\mathrm{degradado}}}{M_{\mathrm{limpo}}}
\]

_Fonte: [templates/tabela_robustez.csv](templates/tabela_robustez.csv)._

**Figura Z — Queda relativa de mAP@0,50** (E03 vs E04). Hipótese H3: E04 apresenta menor \(\Delta\) que E03.

### 4.5 Diagnóstico por imagem

Apresentar exemplos com TP, FP e FN em cenas com alta densidade de leitões (11–15 instâncias). Relacionar FP com possível contagem inflada e FN com subdetecção em sobreposição ou baixa iluminação.

---

## 5. Discussão

### 5.1 Síntese frente às hipóteses

| Hipótese | Resultado (preencher) |
| --- | --- |
| H1 | Autoral vs REF no S1 |
| H2a | v8 vs v5 |
| H2b | v11 vs v8 |
| H3 | YOLO11-R vs YOLO11 degradado |
| H4 | Efeito do % de treino no Recall |

### 5.2 Trade-offs em cenas densas

Discutir equilíbrio entre Recall (cobertura dos leitões) e Precision (caixas espúrias), à luz da homogeneidade de contagem por imagem observada na Etapa 1.

### 5.3 Relação com a literatura

Comparar achados com abordagens de detecção de suínos baseadas em YOLOv5 melhorado [Li and Li 2024] e PLM-YOLOv5 [Peng et al. 2024], destacando que o YOLO11-R adota **protocolo de treino** inspirado nesses trabalhos, sem reimplementação de módulos proprietários.

### 5.4 Limitações

- Tamanho da base (1065 imagens) e classe única.
- Custo computacional de doze experimentos completos (E01–E12).
- Val degradado com conjunto limitado de transformações.

### 5.5 Trabalhos futuros

- Testar variantes maiores (`m`, `l`) se GPU permitir.
- Validação em vídeo ou novas granjas.
- Integração com contagem automática em tempo real.

---

## Nota para integração

- Numerar tabelas e figuras conforme o `.doc` da Etapa 1.
- Inserir valores reais dos CSVs em `templates/` antes da submissão final (Etapa D).
