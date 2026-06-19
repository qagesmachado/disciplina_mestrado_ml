"""Gera o fluxograma metodologico da Etapa 2 em PNG de alta resolucao.

Etapas:
  1. Dados brutos
  2. Analise exploratoria e validacao dos rotulos
  3. Separacao treino/validacao (80/20)
  4. Treinamento dos tres modelos (YOLOv5s, YOLOv8s, YOLO11s)
  5. Validacao dos tres modelos com dados de validacao
  6. Comparacao com metricas de qualidade
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# Paleta
COR_DADOS = "#2E7D9A"
COR_SPLIT = "#4A8FB3"
COR_TREINO = "#3E8E5A"
COR_VAL = "#C77B30"
COR_COMP = "#8E44AD"
COR_TEXTO = "#FFFFFF"
COR_BORDA = "#2C3E50"

fig, ax = plt.subplots(figsize=(16, 8.5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def caixa(x, y, w, h, texto, cor, fontsize=12, bold=True):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.6,rounding_size=2.2",
        linewidth=1.8, edgecolor=COR_BORDA, facecolor=cor, zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x, y, texto, ha="center", va="center", color=COR_TEXTO,
        fontsize=fontsize, fontweight="bold" if bold else "normal",
        zorder=3, wrap=True,
    )


def seta(x1, y1, x2, y2, cor=COR_BORDA, estilo="-"):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=22, linewidth=2.2,
        color=cor, linestyle=estilo, zorder=1,
        shrinkA=2, shrinkB=2,
    )
    ax.add_patch(arr)


def rotulo(x, y, texto, fontsize=11, bold=True):
    ax.text(
        x, y, texto, ha="center", va="center", fontsize=fontsize,
        fontweight="bold" if bold else "normal", color=COR_BORDA, zorder=10,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="none"),
    )

# 1. Dados brutos
caixa(10, 82, 17, 12,
      "1. Dados brutos\n1065 imagens (anotações YOLO)",
      COR_DADOS, fontsize=10.5)

# 2. Analise exploratoria
caixa(35, 82, 22, 16,
      "2. Análise exploratória e validação dos rótulos\n"
      "• Distribuição de leitões por imagem\n"
      "• Verificação das anotações\n"
      "• Consistência dos labels",
      COR_DADOS, fontsize=9)

# 3. Separacao treino/validacao
caixa(62, 82, 22, 12,
      "3. Separação treino/validação\nHold-out 80/20  (seed=42)",
      COR_SPLIT, fontsize=10.5)

# Sub-caixas treino e val
caixa(52, 64, 17, 8, "Treino\n929 imagens (80%)", COR_SPLIT, fontsize=10)
caixa(75, 64, 17, 8, "Validação\n136 imagens (20%)", COR_VAL, fontsize=10)

# 4. Treinamento dos tres modelos
caixa(13, 40, 16, 8, "YOLOv5s\n(E01)", COR_TREINO, fontsize=10)
caixa(13, 30, 16, 8, "YOLOv8s\n(E02)", COR_TREINO, fontsize=10)
caixa(13, 20, 16, 8, "YOLO11s\n(E03)", COR_TREINO, fontsize=10)

# 5. Validacao dos tres modelos
caixa(48, 40, 18, 8, "Avaliar YOLOv5s\nem pig/val", COR_VAL, fontsize=9.5)
caixa(48, 30, 18, 8, "Avaliar YOLOv8s\nem pig/val", COR_VAL, fontsize=9.5)
caixa(48, 20, 18, 8, "Avaliar YOLO11s\nem pig/val", COR_VAL, fontsize=9.5)

# 6. Comparacao
caixa(83, 30, 24, 16,
      "6. Comparação\n\n• Métricas de qualidade\n   de detecção",
      COR_COMP, fontsize=10.5)

# Setas etapa 1 -> 2 -> 3
seta(18.5, 82, 24, 82)
seta(46, 82, 51, 82)
# 3 -> sub-caixas
seta(58, 76, 53, 68)
seta(66, 76, 74, 68)
# treino -> caixas de treinamento
seta(47, 62, 18, 43)
# val -> caixas de validacao (dados de validacao alimentam a avaliacao)
seta(75, 60, 52, 43, cor=COR_VAL, estilo="--")
seta(75, 60, 52, 33, cor=COR_VAL, estilo="--")
seta(75, 60, 52, 23, cor=COR_VAL, estilo="--")

# Cada modelo treinado -> sua validacao
seta(21, 40, 39, 40)
seta(21, 30, 39, 30)
seta(21, 20, 39, 20)

# Validacoes -> comparacao
seta(57, 40, 71, 34)
seta(57, 30, 71, 30)
seta(57, 20, 71, 26)

# Rotulos por cima das setas
rotulo(50, 96, "Metodologia — Detecção de Leitões (YOLOv5s / YOLOv8s / YOLO11s)", fontsize=16)
rotulo(13, 56, "4. Treinamento dos três modelos\n(mesmos hiperparâmetros)", fontsize=10)
rotulo(13, 52, "imgsz=640 | epochs=100 | batch=16 | seed=42", fontsize=9, bold=False)
rotulo(48, 56, "5. Validação no conjunto\nde validação (conf=0,25)", fontsize=10)

# Legenda das setas tracejadas
legenda = [
    Line2D([0], [0], color=COR_VAL, lw=2.2, linestyle="--",
           label="Dados de validação (pig/val) usados na avaliação"),
    Line2D([0], [0], color=COR_BORDA, lw=2.2, linestyle="-",
           label="Fluxo do pipeline"),
]
ax.legend(handles=legenda, loc="lower center", bbox_to_anchor=(0.5, -0.02),
          ncol=2, frameon=False, fontsize=10)

plt.tight_layout()
out = "fluxograma_metodologia.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Figura salva em: {out}")
