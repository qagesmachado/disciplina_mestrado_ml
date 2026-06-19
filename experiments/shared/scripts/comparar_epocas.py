"""Gera gráficos de linha comparando métricas por época (5/10/25/50).

Lê os comparacao_pig_baseline.csv de cada outputs_epoch_* e plota, para cada
métrica, uma curva por modelo (E01/E02/E03) ao longo das épocas.

Uso:
  python experiments/shared/scripts/comparar_epocas.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from comparar import BAR_COLORS, LEGEND_LABELS  # noqa: E402

SHARED_DIR = SCRIPT_DIR.parent
EXPS = ("E01", "E02", "E03")
OUT_DIR = SHARED_DIR / "outputs_epochs" / "figures"


def discover_epochs() -> tuple[int, ...]:
    eps = []
    for d in SHARED_DIR.glob("outputs_epoch_*"):
        if (d / "comparacao_pig_baseline.csv").is_file():
            try:
                eps.append(int(d.name.removeprefix("outputs_epoch_")))
            except ValueError:
                continue
    return tuple(sorted(eps))

# (coluna no CSV, título/eixo Y, nome do arquivo, é métrica 0-1?)
METRICS = (
    ("precision", "Precision", "precision.png", True),
    ("recall", "Recall", "recall.png", True),
    ("map50", "mAP@0.50", "map50.png", True),
    ("map50_95", "mAP@0.50:0.95", "map50_95.png", True),
    ("f1", "F1", "f1.png", True),
    ("total_time_sec", "Total (s)", "total_time_sec.png", False),
    ("ms_per_image", "ms/img", "ms_per_image.png", False),
)


def read_all(epochs) -> dict[int, dict[str, dict[str, str]]]:
    data: dict[int, dict[str, dict[str, str]]] = {}
    for ep in epochs:
        path = SHARED_DIR / f"outputs_epoch_{ep}" / "comparacao_pig_baseline.csv"
        with path.open(encoding="utf-8") as f:
            rows = {row["experimento"]: row for row in csv.DictReader(f)}
        data[ep] = rows
    return data


# Painéis: (coluna, rótulo eixo Y, título, legenda inferior)
DETECCAO_PANEL = (
    ("precision", "Precision", "Precision x épocas", "(a)"),
    ("recall", "Recall", "Recall x épocas", "(b)"),
    ("map50", "mAP@0.50", "mAP@50 x épocas", "(c)"),
    ("map50_95", "mAP@0.50:0.95", "mAP@50:0.95 x épocas", "(d)"),
)
PERFORMANCE_PANEL = (
    ("ms_per_image", "ms/img", "ms/img x épocas", "(a)"),
    ("total_time_sec", "Total (s)", "Total (s) x épocas", "(b)"),
)


def _draw_curve(ax, data, epochs, key) -> None:
    from matplotlib.ticker import ScalarFormatter

    for i, eid in enumerate(EXPS):
        ys = [float(data[ep][eid][key]) for ep in epochs]
        ax.plot(epochs, ys, marker="o", color=BAR_COLORS[i], label=LEGEND_LABELS[eid])
    ax.set_xlabel("Épocas de treinamento")
    ax.set_xscale("log")
    ax.set_xticks(epochs)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.minorticks_off()
    ax.grid(True, alpha=0.3)
    ax.legend()


def plot_metric(data, epochs, key, title, fname, is_ratio) -> Path:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.5))
    _draw_curve(ax, data, epochs, key)
    ax.set_ylabel(title)
    ax.set_title(f"{title} x épocas")
    fig.tight_layout()

    out = OUT_DIR / fname
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_panel(data, epochs, specs, fname, nrows, ncols, figsize) -> Path:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten()
    for ax, (key, ylabel, title, caption) in zip(axes, specs):
        _draw_curve(ax, data, epochs, key)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.text(0.5, -0.15, caption, transform=ax.transAxes, ha="center", va="top",
                fontsize=13, fontweight="bold")

    for ax in axes[len(specs):]:
        ax.axis("off")

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.30)
    out = OUT_DIR / fname
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def write_tables(data, epochs) -> Path:
    lines = [
        "# Métricas por época — pig/val (136 imagens)",
        "",
        "Uma tabela por métrica. Linhas = épocas de treinamento; "
        "colunas = E01 YOLOv5s, E02 YOLOv8s, E03 YOLO11s.",
    ]
    for key, title, _fname, is_ratio in METRICS:
        fmt = "{:.4f}" if is_ratio else "{:.1f}"
        lines += [
            "",
            f"## {title}",
            "",
            "| Épocas | E01 YOLOv5s | E02 YOLOv8s | E03 YOLO11s |",
            "| ---: | ---: | ---: | ---: |",
        ]
        for ep in epochs:
            vals = " | ".join(fmt.format(float(data[ep][eid][key])) for eid in EXPS)
            lines.append(f"| {ep} | {vals} |")

    out = SHARED_DIR / "outputs_epochs" / "tabelas_epocas.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    epochs = discover_epochs()
    if not epochs:
        raise SystemExit("Nenhuma pasta outputs_epoch_* com comparacao_pig_baseline.csv encontrada.")
    print(f"Épocas encontradas: {', '.join(map(str, epochs))}")
    data = read_all(epochs)
    for key, title, fname, is_ratio in METRICS:
        out = plot_metric(data, epochs, key, title, fname, is_ratio)
        print(f"[OK] {out}")
    print(f"[OK] {plot_panel(data, epochs, DETECCAO_PANEL, 'metricas_deteccao_painel.png', 2, 2, (13, 10))}")
    print(f"[OK] {plot_panel(data, epochs, PERFORMANCE_PANEL, 'metricas_performance_painel.png', 1, 2, (13, 5))}")
    print(f"[OK] {write_tables(data, epochs)}")


if __name__ == "__main__":
    main()
