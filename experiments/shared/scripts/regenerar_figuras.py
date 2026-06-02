"""Regenera as figuras G1/G2 a partir do CSV consolidado.

Util quando os metrics_summary.csv por experimento nao estao presentes,
mas existe experiments/shared/outputs/comparacao_pig_baseline.csv.

Uso:
  python experiments/shared/scripts/regenerar_figuras.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from comparar import plot_comparison  # noqa: E402

CSV_PATH = SCRIPT_DIR.parent / "outputs" / "comparacao_pig_baseline.csv"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    metrics = {row["experimento"]: row for row in rows}
    compare_exps = tuple(row["experimento"] for row in rows)

    figures = plot_comparison(metrics, compare_exps)
    for fig in figures:
        print(f"[OK] {fig}")


if __name__ == "__main__":
    main()
