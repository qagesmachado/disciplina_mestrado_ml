"""
Treino YOLOv5 (E01) — venv_yolo_5.

Uso:
  python experiments/YOLO_V5/scripts/treinar.py E01
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_SCRIPTS = SCRIPT_DIR.parent.parent / "shared" / "scripts"
for p in (str(SHARED_SCRIPTS), str(SCRIPT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from config_loader import get_experiment, resolve_weights  # noqa: E402
from device_utils import adjust_batch_for_device, adjust_workers_for_device, resolve_device  # noqa: E402
from experiment_log import write_experiment_log  # noqa: E402
from paths import REPO_ROOT  # noqa: E402


def train_yolov5(exp: dict, epochs: int, batch: int, device: str, workers: int) -> Path:
    output_dir = exp["output_dir"]
    weights = resolve_weights(exp["weights_init"])
    data_yaml = exp["data_yaml"]

    if not data_yaml.is_file():
        raise FileNotFoundError(
            f"YAML de dados não encontrado: {data_yaml}\n"
            "Execute: python experiments/shared/scripts/ensure_pig_dataset.py"
        )

    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_yolov5_cli.py"),
        "train",
        "--data",
        str(data_yaml),
        "--weights",
        str(weights),
        "--imgsz",
        str(exp["imgsz"]),
        "--epochs",
        str(epochs),
        "--batch",
        str(batch),
        "--patience",
        str(exp["patience"]),
        "--seed",
        str(exp["seed"]),
        "--workers",
        str(workers),
        "--project",
        str(output_dir.parent),
        "--name",
        output_dir.name,
        "--exist-ok",
    ]
    if device:
        cmd.extend(["--device", device])

    print("[INFO] Treino YOLOv5:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(REPO_ROOT), env=os.environ.copy())

    best_pt = output_dir / "weights" / "best.pt"
    if not best_pt.is_file():
        raise FileNotFoundError(f"Checkpoint não gerado: {best_pt}")
    return best_pt


def main() -> None:
    parser = argparse.ArgumentParser(description="Treino YOLOv5 (E01)")
    parser.add_argument("exp_id", help="E01 (REF não treina)")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()

    exp = get_experiment(args.exp_id.upper())

    if args.exp_id.upper() == "REF" or exp.get("train") is False:
        print("[INFO] REF não requer treino; use validar.py REF")
        return

    if exp.get("framework") != "yolov5":
        raise SystemExit(f"{exp['id']} não pertence a YOLO_V5. Use experiments/YOLO_V8/scripts/")

    epochs = args.epochs if args.epochs is not None else int(exp["epochs"])
    batch = args.batch if args.batch is not None else int(exp["batch"])
    device_requested = args.device if args.device is not None else str(exp.get("device", "auto"))
    workers = args.workers if args.workers is not None else int(exp.get("workers", 4))
    batch_cpu = int(exp.get("batch_cpu", 8))

    try:
        import yolov5  # noqa: F401
        import torch

        device, device_msg = resolve_device(device_requested)
        batch = adjust_batch_for_device(batch, device, batch_cpu)
        workers = adjust_workers_for_device(workers, device)
        print(f"[INFO] {device_msg}")

        log_lines = [
            f"exp_id={exp['id']}",
            f"framework=yolov5",
            f"run_name={exp['run_name']}",
            f"data_yaml={exp['data_yaml']}",
            f"weights_init={exp['weights_init']}",
            f"epochs={epochs} batch={batch} imgsz={exp['imgsz']} seed={exp['seed']}",
            f"device={device}",
            f"yolov5={getattr(yolov5, '__version__', '7.x')}",
            f"torch={torch.__version__}",
        ]
    except ImportError as err:
        raise SystemExit("Ative venv_yolo_5: pip install -r requirements-yolov5.txt") from err

    best_pt = train_yolov5(exp, epochs, batch, device, workers)
    log_lines.append(f"best.pt={best_pt}")
    write_experiment_log(exp["output_dir"], log_lines)
    print(f"[OK] Treino concluído: {best_pt}")


if __name__ == "__main__":
    main()
