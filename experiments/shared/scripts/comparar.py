"""
Compara E01, E02 e E03 (se validados).

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
    "E03": ("YOLO11s autoral", "E03"),
}

ALL_COMPARE_IDS = ("E01", "E02", "E03")
OPTIONAL_COMPARE_IDS = ("E02", "E03")
VALIDATE_HINTS = {
    "E01": "python experiments/YOLO_V5/scripts/validar_yolov5.py E01",
    "E02": "python experiments/YOLO_V8/scripts/validar.py E02",
    "E03": "python experiments/YOLO_V11/scripts/validar.py E03",
}

METRICS_GLOSSARY = """
## O que significa cada métrica

Contexto: **detecção de objetos** em `pig/val`, 136 imagens, `conf=0,25`.

### Precision (P)

Das detecções emitidas pelo modelo, quantas caixas estão corretas (IoU ≥ 0,50 com algum ground truth).

### Recall (R)

Dos objetos anotados no ground truth, quantos foram detectados.

### F1

Média harmônica entre Precision e Recall — resume o equilíbrio entre acertar sem errar (P) e não deixar passar (R):

```
F1 = 2 × P × R / (P + R)
```

No pipeline, P e R vêm do `model.val()` (Ultralytics); F1 é calculado em `metrics_utils.f1_score` a partir desses valores (não é exportado diretamente pelo Ultralytics).

### mAP@0.50 / mAP@0.50:0.95

Métricas principais de detecção (consideram ranking de confiança e, no mAP@0.50:0.95, vários limiares de IoU). F1 complementa P e R, mas não substitui mAP na análise principal.

### Leitura rápida

- **mAP@0,50 ~0,99** — saturado para modelos maduros no pig/val.
- **F1 ~0,97–0,99** — próximo de P e R quando ambos são altos.
- Análise TCD: `entrega_parte_2/apoio_metricas.md`
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


def _has_validation(exp_id: str) -> bool:
    try:
        exp = get_experiment(exp_id)
    except KeyError:
        return False
    return (exp["output_dir"] / "val" / "metrics_summary.csv").is_file()


def resolve_compare_exps() -> tuple[str, ...]:
    exps: list[str] = []
    missing: list[str] = []
    for eid in ALL_COMPARE_IDS:
        if _has_validation(eid):
            exps.append(eid)
        else:
            missing.append(eid)

    for eid in missing:
        print(f"[AVISO] {eid} sem validação — omitido da comparação.")
        if hint := VALIDATE_HINTS.get(eid):
            print(f"         Rode: {hint}")

    if not exps:
        raise SystemExit(
            "Nenhum experimento validado (E01/E02/E03).\n"
            "Rode treinar + validar de pelo menos um experimento antes de comparar."
        )

    if "E01" in missing:
        print("[AVISO] E01 ausente — comparação parcial (sem baseline YOLOv5 / H1).")

    return tuple(exps)


def read_metrics(exp_id: str) -> dict[str, str]:
    exp = get_experiment(exp_id)
    path = exp["output_dir"] / "val" / "metrics_summary.csv"
    if not path.is_file():
        hints = {
            "E01": "experiments/YOLO_V5/scripts/validar_yolov5.py E01",
            **VALIDATE_HINTS,
        }
        raise FileNotFoundError(f"Sem validação para {exp_id}: {path}\nRode: {hints.get(exp_id, '')}")
    with path.open(encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    if not row.get("f1"):
        row["f1"] = str(round(f1_score(float(row["precision"]), float(row["recall"])), 6))
    return row


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
        "Modelos autorais E01–E03. Mesmo conjunto de **validação** (`pig/val`, 136 imagens).",
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

    if "E01" in compare_exps and "E02" in compare_exps:
        lines.append("")
        lines.extend(_delta_table("E02", "E01", metrics, "H1 — E02 vs E01 (YOLOv8 vs YOLOv5)"))
    if "E02" in compare_exps and "E03" in compare_exps:
        lines.append("")
        lines.extend(_delta_table("E03", "E02", metrics, "H2 — E03 vs E02 (YOLO11 vs YOLOv8)"))

    figure_lines = _figure_markdown_lines(compare_exps, has_time=any(metrics[e].get("total_time_sec") for e in compare_exps))
    lines.extend(["", *figure_lines, "", METRICS_GLOSSARY])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


LEGEND_LABELS = {
    "E01": "E01 YOLOv5s",
    "E02": "E02 YOLOv8s",
    "E03": "E03 YOLO11s",
}

BAR_COLORS = ("#1f77b4", "#ff7f0e", "#2ca02c")

METRIC_SPECS: tuple[tuple[str, str, str], ...] = (
    ("precision", "Precision", "G1_precision.png"),
    ("recall", "Recall", "G1_recall.png"),
    ("map50", "mAP@0.50", "G1_map50.png"),
    ("map50_95", "mAP@0.50:0.95", "G1_map50_95.png"),
)

TIME_SPECS: tuple[tuple[str, str, str], ...] = (
    ("total_time_sec", "Total (s)", "G2_total_time_sec.png"),
    ("ms_per_image", "ms/imagem", "G2_ms_per_image.png"),
    ("val_time_sec", "Val (s)", "G2_val_time_sec.png"),
    ("detect_time_sec", "Detect (s)", "G2_detect_time_sec.png"),
    ("match_time_sec", "Match (s)", "G2_match_time_sec.png"),
)


FIGURE_AXIS_X = (
    "Modelo treinado e validado no mesmo `pig/val` (136 imagens): "
    "**E01 YOLOv5s** (azul), **E02 YOLOv8s** (laranja), **E03 YOLO11s** (verde)."
)

FIGURE_SPECS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "G1_precision.png",
        "Precision",
        "Valor",
        "0 a 1 (quanto maior, melhor)",
        "Das caixas preditas pelo modelo, qual fração está correta (IoU ≥ 0,50 com ground truth). "
        "Mede **confiabilidade** das detecções — poucos falsos positivos.",
    ),
    (
        "G1_recall.png",
        "Recall",
        "Valor",
        "0 a 1 (quanto maior, melhor)",
        "Dos leitões anotados no ground truth, qual fração foi detectada. "
        "Mede **cobertura** — poucos falsos negativos (leitões não vistos).",
    ),
    (
        "G1_map50.png",
        "mAP@0.50",
        "Valor",
        "0 a 1 (quanto maior, melhor)",
        "Mean Average Precision com IoU mínimo de 0,50. Resume precisão e recall "
        "considerando o **ranking de confiança** das detecções.",
    ),
    (
        "G1_map50_95.png",
        "mAP@0.50:0.95",
        "Valor",
        "0 a 1 (quanto maior, melhor)",
        "mAP médio em vários limiares de IoU (0,50 a 0,95). Métrica **mais exigente** que mAP@0,50 — "
        "penaliza caixas imprecisas mesmo quando a classe está correta.",
    ),
    (
        "G2_total_time_sec.png",
        "Tempo total de validação",
        "Tempo (s)",
        "Segundos (quanto menor, mais rápido)",
        "Tempo do pipeline completo de validação: métricas globais + inferência por imagem + "
        "cálculo TP/FP/FN. Inclui `val` + `detect` + `match`.",
    ),
    (
        "G2_ms_per_image.png",
        "Tempo por imagem",
        "Tempo",
        "Milissegundos por imagem (quanto menor, mais rápido)",
        "Custo médio por frame: `total_time_sec ÷ 136 × 1000`. Útil para comparar "
        "**velocidade em produção** (vídeo/tempo real).",
    ),
    (
        "G2_val_time_sec.png",
        "Tempo do val",
        "Tempo (s)",
        "Segundos (quanto menor, mais rápido)",
        "Tempo da etapa `model.val()` / `yolov5.val` — calcula precision, recall e mAP "
        "no conjunto de validação de uma vez.",
    ),
    (
        "G2_detect_time_sec.png",
        "Tempo do detect",
        "Tempo (s)",
        "Segundos (quanto menor, mais rápido)",
        "Tempo da inferência imagem a imagem (`detect`) para gerar labels preditas "
        "usadas no CSV `per_image_tp_fp_fn.csv`.",
    ),
    (
        "G2_match_time_sec.png",
        "Tempo do match",
        "Tempo (s)",
        "Segundos (quanto menor, mais rápido)",
        "Tempo para comparar predições vs ground truth por imagem (IoU, TP/FP/FN). "
        "Etapa leve em CPU; não envolve rede neural.",
    ),
)


def _figure_markdown_lines(compare_exps: tuple[str, ...], *, has_time: bool) -> list[str]:
    if len(compare_exps) < 2:
        return ["## Gráficos individuais", "", "Disponíveis após validar E01–E03."]

    lines = [
        "## Gráficos individuais",
        "",
        "Um arquivo PNG por parâmetro em `experiments/shared/outputs/figures/`. "
        "Todos compartilham a mesma estrutura de barras.",
        "",
        "### Eixos (todos os gráficos)",
        "",
        f"- **Eixo X:** {FIGURE_AXIS_X}",
        "- **Eixo Y:** valor numérico da métrica ou do tempo medido na validação "
        "(rótulo *Valor* ou *Tempo* no gráfico).",
        "",
        "### Métricas de detecção (série G1)",
        "",
    ]

    for fname, title, ylabel, y_range, meaning in FIGURE_SPECS[:4]:
        lines.extend(
            [
                f"#### `{fname}` — {title}",
                "",
                f"- **Arquivo:** `experiments/shared/outputs/figures/{fname}`",
                f"- **O que mostra:** {meaning}",
                f"- **Eixo X:** modelo (E01 / E02 / E03)",
                f"- **Eixo Y:** {ylabel} — escala {y_range}",
                "",
            ]
        )

    if has_time:
        lines.extend(["### Tempos de validação (série G2)", ""])
        for fname, title, ylabel, y_range, meaning in FIGURE_SPECS[4:]:
            lines.extend(
                [
                    f"#### `{fname}` — {title}",
                    "",
                    f"- **Arquivo:** `experiments/shared/outputs/figures/{fname}`",
                    f"- **O que mostra:** {meaning}",
                    f"- **Eixo X:** modelo (E01 / E02 / E03)",
                    f"- **Eixo Y:** {ylabel} — escala {y_range}",
                    "",
                ]
            )

    lines.extend(
        [
            "### Como ler",
            "",
            "- Barras **mais altas** nos gráficos G1 indicam **melhor desempenho** de detecção.",
            "- Barras **mais baixas** nos gráficos G2 indicam **validação mais rápida**.",
            "- Compare sempre os três modelos no **mesmo gráfico** — mesma métrica, mesmo split, `conf=0,25`.",
        ]
    )
    return lines


def _plot_single_metric(
    metrics: dict[str, dict[str, str]],
    compare_exps: tuple[str, ...],
    *,
    key: str,
    label: str,
    ylabel: str,
    output_path: Path,
    ylim: tuple[float, float] | None = None,
    value_fmt: str = "{:.4f}",
) -> None:
    import matplotlib.pyplot as plt

    model_labels = [LEGEND_LABELS.get(eid, eid) for eid in compare_exps]
    vals = [float(metrics[eid][key]) for eid in compare_exps]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(model_labels, vals, color=BAR_COLORS[: len(compare_exps)], width=0.55)
    ax.set_ylabel(ylabel)
    ax.set_title(f"pig/val — {label}")
    ax.grid(True, axis="y", alpha=0.3)
    if ylim is not None:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(0, max(vals) * 1.15 if vals else 1)
    ax.bar_label(
        bars,
        labels=[value_fmt.format(v) for v in vals],
        padding=3,
        fontsize=10,
        fontweight="bold",
    )
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_comparison(metrics: dict[str, dict[str, str]], compare_exps: tuple[str, ...]) -> list[Path]:
    out_dir = comparison_outputs_dir() / "figures"
    generated: list[Path] = []

    for key, label, fname in METRIC_SPECS:
        out = out_dir / fname
        _plot_single_metric(
            metrics,
            compare_exps,
            key=key,
            label=label,
            ylabel="Valor",
            output_path=out,
            ylim=(0, 1.05),
        )
        generated.append(out)

    if any(metrics[e].get("total_time_sec") for e in compare_exps):
        for key, label, fname in TIME_SPECS:
            out = out_dir / fname
            _plot_single_metric(
                metrics,
                compare_exps,
                key=key,
                label=label,
                ylabel="Tempo",
                output_path=out,
                value_fmt="{:.1f}",
            )
            generated.append(out)

    return generated


def main() -> None:
    compare_exps = resolve_compare_exps()
    metrics = {eid: read_metrics(eid) for eid in compare_exps}
    write_outputs(metrics, compare_exps)
    figures = plot_comparison(metrics, compare_exps)

    out_md = comparison_outputs_dir() / "comparacao_pig_baseline.md"
    for eid in compare_exps:
        m = metrics[eid]
        print(
            f"  {eid}: R={float(m['recall']):.4f}  mAP50={float(m['map50']):.4f}  "
            f"mAP50-95={float(m['map50_95']):.4f}"
        )
    print(f"\n[OK] {out_md}")
    for fig in figures:
        print(f"[OK] {fig}")


if __name__ == "__main__":
    main()

