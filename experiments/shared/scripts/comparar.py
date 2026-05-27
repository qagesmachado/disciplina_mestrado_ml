"""
Compara E01, E02 (se validado) e REF; atualiza tabela do artigo.

Uso:
  python experiments/shared/scripts/comparar.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from config_loader import comparison_outputs_dir, get_experiment  # noqa: E402
from metrics_utils import f1_score  # noqa: E402
from paths import ENTREGA_TEMPLATES, YOLO_V8_ROOT  # noqa: E402

METRIC_COLS = ("precision", "recall", "map50", "map50_95", "f1")
TIME_COLS = (
    "total_time_sec",
    "ms_per_image",
    "val_time_sec",
    "detect_time_sec",
    "match_time_sec",
    "device",
)

EXP_DISPLAY = {
    "E01": ("YOLOv5s autoral", "E01"),
    "E02": ("YOLOv8s autoral", "E02"),
    "REF": ("best.pt (terceiros)", "REF"),
}

METRICS_GLOSSARY = """
## O que significa cada métrica

Contexto: **detecção de objetos** em `pig/val`, 136 imagens, `conf=0,25`.

### mAP@0.50 / mAP@0.50:0.95

Métricas principais de detecção.

### Leitura rápida

- **mAP@0,50 ~0,99** — saturado para modelos maduros no pig/val.
- Análise TCD: `entrega_parte_b_c/analise_desempenho_baseline.md`
""".strip()


def _fmt_time(row: dict[str, str], key: str) -> str:
    v = row.get(key, "").strip()
    if not v:
        return "—"
    if key == "device":
        return v
    try:
        return f"{float(v):.3f}" if key.endswith("_sec") else f"{float(v):.1f}"
    except ValueError:
        return v


def resolve_compare_exps() -> tuple[str, ...]:
    base = ("E01", "REF")
    e02_path = YOLO_V8_ROOT / "outputs" / "E02_yolov8s_pig" / "val" / "metrics_summary.csv"
    if e02_path.is_file():
        return ("E01", "E02", "REF")
    print("[AVISO] E02 sem validação — comparando apenas E01 e REF.")
    print("         Rode: python experiments/YOLO_V8/scripts/validar.py E02")
    return base


def read_metrics(exp_id: str) -> dict[str, str]:
    exp = get_experiment(exp_id)
    path = exp["output_dir"] / "val" / "metrics_summary.csv"
    if not path.is_file():
        hints = {
            "E01": "experiments/YOLO_V5/scripts/validar.py E01",
            "REF": "experiments/YOLO_V5/scripts/validar.py REF",
            "E02": "experiments/YOLO_V8/scripts/validar.py E02",
        }
        raise FileNotFoundError(f"Sem validação para {exp_id}: {path}\nRode: {hints.get(exp_id, '')}")
    with path.open(encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    if not row.get("f1"):
        row["f1"] = str(round(f1_score(float(row["precision"]), float(row["recall"])), 6))
    return row


def update_tabela_resultados(rows: dict[str, dict[str, str]]) -> None:
    csv_path = ENTREGA_TEMPLATES / "tabela_resultados_s1.csv"
    notas_map = {
        "REF": "dataset pig fixo (136 val)",
        "E02": "treino pig/train (YOLO_V8)",
        "E01": "treino pig/train (YOLO_V5)",
    }
    updated: list[dict[str, str]] = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            eid = row.get("experimento", "").strip().upper()
            if eid in rows:
                src = rows[eid]
                row["precision"] = src["precision"]
                row["recall"] = src["recall"]
                row["map50"] = src["map50"]
                row["map50_95"] = src["map50_95"]
                if "f1" in fieldnames:
                    row["f1"] = src["f1"]
                row["split"] = "pig_val"
                if "notas" in fieldnames:
                    row["notas"] = notas_map.get(eid, "treino pig/train")
            updated.append(row)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(updated)


def _metric_table_row(eid: str, m: dict[str, str]) -> str:
    label, _ = EXP_DISPLAY.get(eid, (m.get("modelo", eid), eid))
    return (
        f"| {label} | {eid} | {float(m['precision']):.4f} | {float(m['recall']):.4f} | "
        f"{float(m['map50']):.4f} | {float(m['map50_95']):.4f} | {float(m['f1']):.4f} |"
    )


def _delta_table(eid_a: str, eid_b: str, metrics: dict[str, dict[str, str]], title: str) -> list[str]:
    a, b = metrics[eid_a], metrics[eid_b]
    lines = [
        f"## {title}",
        "",
        f"| Métrica | {eid_a} | {eid_b} | Δ ({eid_a} − {eid_b}) |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, label in [
        ("precision", "Precision"),
        ("recall", "Recall"),
        ("map50", "mAP@0.50"),
        ("map50_95", "mAP@0.50:0.95"),
        ("f1", "F1"),
    ]:
        va, vb = float(a[key]), float(b[key])
        lines.append(f"| {label} | {va:.4f} | {vb:.4f} | {va - vb:+.4f} |")
    return lines


def write_outputs(metrics: dict[str, dict[str, str]], compare_exps: tuple[str, ...]) -> None:
    out_dir = comparison_outputs_dir()
    csv_path = out_dir / "comparacao_pig_baseline.csv"
    md_path = out_dir / "comparacao_pig_baseline.md"

    fieldnames = ["experimento", "modelo", "split", *METRIC_COLS, *TIME_COLS]
    rows_out = [
        {
            "experimento": eid,
            "modelo": metrics[eid].get("modelo", ""),
            "split": "pig_val (136 imgs)",
            **{k: metrics[eid].get(k, "") for k in METRIC_COLS},
            **{k: metrics[eid].get(k, "") for k in TIME_COLS},
        }
        for eid in compare_exps
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    lines = [
        "# Comparação — dataset pig fixo (train/val Kaggle)",
        "",
        "Mesmo conjunto de **validação** (`pig/val`, 136 imagens).",
        "",
        "| Modelo | Exp | Precision | Recall | mAP@0.50 | mAP@0.50:0.95 | F1 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for eid in compare_exps:
        lines.append(_metric_table_row(eid, metrics[eid]))

    if any(metrics[e].get("total_time_sec") for e in compare_exps):
        lines.extend(
            [
                "",
                "## Tempo de validação",
                "",
                "| Modelo | Exp | Total (s) | ms/img | device |",
                "| --- | --- | ---: | ---: | --- |",
            ]
        )
        for eid in compare_exps:
            m = metrics[eid]
            label, _ = EXP_DISPLAY.get(eid, (eid, eid))
            lines.append(
                f"| {label} | {eid} | {_fmt_time(m, 'total_time_sec')} | "
                f"{_fmt_time(m, 'ms_per_image')} | {_fmt_time(m, 'device')} |"
            )

    lines.extend(_delta_table("E01", "REF", metrics, "H1 — E01 vs REF"))
    if "E02" in compare_exps:
        lines.append("")
        lines.extend(_delta_table("E02", "E01", metrics, "H2a — E02 vs E01 (YOLOv8 vs YOLOv5)"))

    lines.extend(
        [
            "",
            "Gráfico: `experiments/shared/outputs/figures/G1_pig_baseline.png`",
            "",
            METRICS_GLOSSARY,
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_comparison(metrics: dict[str, dict[str, str]], compare_exps: tuple[str, ...]) -> None:
    import matplotlib.pyplot as plt

    out_dir = comparison_outputs_dir() / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    labels_x = ["Precision", "Recall", "mAP@0.50", "mAP@0.50:0.95"]
    keys = ["precision", "recall", "map50", "map50_95"]
    n = len(compare_exps)
    w = 0.8 / n
    x = range(len(labels_x))
    fig, ax = plt.subplots(figsize=(10, 5))

    legend_labels = {"E01": "E01 YOLOv5s", "E02": "E02 YOLOv8s", "REF": "REF best.pt"}
    for i, eid in enumerate(compare_exps):
        vals = [float(metrics[eid][k]) for k in keys]
        offset = (i - (n - 1) / 2) * w
        ax.bar([xi + offset for xi in x], vals, width=w, label=legend_labels.get(eid, eid))

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels_x)
    ax.set_ylabel("Valor")
    ax.set_title("pig/val — comparação de modelos")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    out = out_dir / "G1_pig_baseline.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main() -> None:
    compare_exps = resolve_compare_exps()
    metrics = {eid: read_metrics(eid) for eid in compare_exps}
    write_outputs(metrics, compare_exps)
    update_tabela_resultados(metrics)
    plot_comparison(metrics, compare_exps)

    out_md = comparison_outputs_dir() / "comparacao_pig_baseline.md"
    for eid in compare_exps:
        m = metrics[eid]
        print(
            f"  {eid}: R={float(m['recall']):.4f}  mAP50={float(m['map50']):.4f}  "
            f"mAP50-95={float(m['map50_95']):.4f}"
        )
    print(f"\n[OK] {out_md}")


if __name__ == "__main__":
    main()
