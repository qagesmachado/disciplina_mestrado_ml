"""Gera o fluxograma metodologico da Etapa 2 em PNG de alta resolucao.

Etapas:
  1. Dados brutos
  2. Separacao treino/validacao (80/20)
  3. Treinamento dos tres modelos (YOLOv5s, YOLOv8s, YOLO11s)
  4. Validacao dos tres modelos com dados de validacao
  5. Comparacao com graficos e metricas
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

fig, ax = plt.subplots(figsize=(15, 8.5))
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


# Titulo
ax.text(
    50, 96, "Metodologia — Detecção de Leitões (YOLOv5s / YOLOv8s / YOLO11s)",
    ha="center", va="center", fontsize=16, fontweight="bold", color=COR_BORDA,
)

# 1. Dados brutos
caixa(15, 82, 24, 12,
      "1. Dados brutos\n1065 imagens (anotações YOLO)",
      COR_DADOS, fontsize=11)

# 2. Separacao treino/validacao
caixa(50, 82, 26, 12,
      "2. Separação treino/validação\nHold-out 80/20  (seed=42)",
      COR_SPLIT, fontsize=11)

# Sub-caixas treino e val
caixa(40, 64, 17, 8, "Treino\n929 imagens (80%)", COR_SPLIT, fontsize=10)
caixa(63, 64, 17, 8, "Validação\n136 imagens (20%)", COR_VAL, fontsize=10)

# 3. Treinamento dos tres modelos
ax.text(20, 52, "3. Treinamento dos três modelos",
        ha="center", va="center", fontsize=12, fontweight="bold", color=COR_BORDA)
caixa(13, 44, 16, 8, "YOLOv5s\n(E01)", COR_TREINO, fontsize=10)
caixa(13, 34, 16, 8, "YOLOv8s\n(E02)", COR_TREINO, fontsize=10)
caixa(13, 24, 16, 8, "YOLO11s\n(E03)", COR_TREINO, fontsize=10)

# 4. Validacao dos tres modelos
ax.text(50, 52, "4. Validação no conjunto de validação (conf=0,25)",
        ha="center", va="center", fontsize=12, fontweight="bold", color=COR_BORDA)
caixa(48, 44, 18, 8, "Avaliar YOLOv5s\nem pig/val", COR_VAL, fontsize=9.5)
caixa(48, 34, 18, 8, "Avaliar YOLOv8s\nem pig/val", COR_VAL, fontsize=9.5)
caixa(48, 24, 18, 8, "Avaliar YOLO11s\nem pig/val", COR_VAL, fontsize=9.5)

# 5. Comparacao
caixa(83, 34, 26, 22,
      "5. Comparação\n\n• Métricas de qualidade\n   de detecção\n• Métricas de desempenho\n   computacional",
      COR_COMP, fontsize=10.5)

# Setas etapa 1 -> 2
seta(27, 82, 37, 82)
# 2 -> sub-caixas
seta(46, 76, 41, 68)
seta(54, 76, 62, 68)
# treino -> caixas de treinamento
seta(36, 62, 18, 47)
# val -> caixas de validacao (dados de validacao alimentam a avaliacao)
seta(63, 60, 52, 47, cor=COR_VAL, estilo="--")
seta(63, 60, 52, 37, cor=COR_VAL, estilo="--")
seta(63, 60, 52, 27, cor=COR_VAL, estilo="--")

# Cada modelo treinado -> sua validacao
seta(21, 44, 39, 44)
seta(21, 34, 39, 34)
seta(21, 24, 39, 24)

# Validacoes -> comparacao
seta(57, 44, 70, 38)
seta(57, 34, 70, 34)
seta(57, 24, 70, 30)

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
