"""
Executa yolov5.train | val | detect com patches de compatibilidade (PyTorch 2.6+).

Uso:
  python experiments/YOLO_V5/scripts/run_yolov5_cli.py train --data ...
"""
from __future__ import annotations

import runpy
import sys

from yolov5_compat import apply_all_yolov5_compat

apply_all_yolov5_compat()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Uso: run_yolov5_cli.py <train|val|detect> [args...]")

    subcommand = sys.argv[1]
    if subcommand not in {"train", "val", "detect"}:
        raise SystemExit(f"Subcomando inválido: {subcommand}")

    sys.argv = [f"yolov5.{subcommand}", *sys.argv[2:]]
    runpy.run_module(f"yolov5.{subcommand}", run_name="__main__")
