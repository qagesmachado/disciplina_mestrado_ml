"""Relatório HTML de validação."""
from __future__ import annotations

from pathlib import Path


def write_html_report(
    output_dir: Path,
    exp_id: str,
    summary_row: dict[str, object],
    per_image_csv: Path,
    summary_csv: Path,
    script_label: str = "validar.py",
) -> None:
    html_path = output_dir / "val_report.html"
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <title>Validação {exp_id}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    table {{ border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border: 1px solid #ccc; padding: 8px 10px; }}
    th {{ background: #f3f3f3; }}
  </style>
</head>
<body>
  <h1>Validação — {exp_id}</h1>
  <p>Gerado por <code>{script_label}</code></p>
  <table>
    <tr><th>Precision</th><th>Recall</th><th>mAP@0.50</th><th>mAP@0.50:0.95</th><th>F1</th></tr>
    <tr>
      <td>{summary_row["precision"]}</td>
      <td>{summary_row["recall"]}</td>
      <td>{summary_row["map50"]}</td>
      <td>{summary_row["map50_95"]}</td>
      <td>{summary_row["f1"]}</td>
    </tr>
  </table>
  <p><strong>Tempo de validação:</strong> total {summary_row.get("total_time_sec", "—")} s
  ({summary_row.get("ms_per_image", "—")} ms/imagem, n={summary_row.get("n_val_images", "—")})</p>
  <p>Detalhe: val {summary_row.get("val_time_sec", "—")} s,
  detect {summary_row.get("detect_time_sec", "—")} s,
  pareamento TP/FP/FN {summary_row.get("match_time_sec", "—")} s
  (device: {summary_row.get("device", "—")})</p>
  <ul>
    <li><code>{per_image_csv}</code></li>
    <li><code>{summary_csv}</code></li>
  </ul>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
