"""
Atalho legado (Etapa 1) — valida REF e compara.

Prefira:
  python experiments/YOLO_V5/scripts/validar.py REF
  python experiments/shared/scripts/comparar.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    print("[INFO] Atalho: validar REF + comparar\n")
    for cmd in (
        [sys.executable, str(ROOT / "experiments/YOLO_V5/scripts/validar.py"), "REF"],
        [sys.executable, str(ROOT / "experiments/shared/scripts/comparar.py")],
    ):
        subprocess.run(cmd, check=True, cwd=str(ROOT))


if __name__ == "__main__":
    main()
