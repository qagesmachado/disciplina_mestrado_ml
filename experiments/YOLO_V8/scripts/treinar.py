"""
Treino YOLOv8 (E02) — venv_yolo_ultralytics.

Uso:
  python experiments/YOLO_V8/scripts/treinar.py E02
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_SCRIPTS = SCRIPT_DIR.parent.parent / "shared" / "scripts"
for p in (str(SHARED_SCRIPTS), str(SCRIPT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from config_loader import get_experiment  # noqa: E402
from device_utils import adjust_batch_for_device, resolve_device  # noqa: E402
from experiment_log import write_experiment_log  # noqa: E402


def train_ultralytics(exp: dict, epochs: int, batch: int, imgsz: int, device: str) -> Path:
    from ultralytics import YOLO

    output_dir = exp["output_dir"]
    data_yaml = exp["data_yaml"]
    weights = exp["weights_init"]

    if not data_yaml.is_file():
        raise FileNotFoundError(
            f"YAML não encontrado: {data_yaml}\n"
            "Execute: python experiments/shared/scripts/ensure_pig_dataset.py"
        )

    model = YOLO(weights)
    print(f"[INFO] Treino Ultralytics {exp['id']}: {weights} -> {output_dir.name}")
    model.train(
        data=str(data_yaml),
        imgsz=imgsz,
        epochs=epochs,
        batch=batch,
        patience=int(exp["patience"]),
        seed=int(exp["seed"]),
        project=str(output_dir.parent),
        name=output_dir.name,
        exist_ok=True,
        device=device,
        verbose=True,
    )

    best_pt = output_dir / "weights" / "best.pt"
    if not best_pt.is_file():
        raise FileNotFoundError(f"Checkpoint não gerado: {best_pt}")
    return best_pt


def main() -> None:
    parser = argparse.ArgumentParser(description="Treino Ultralytics (E02)")
    parser.add_argument("exp_id", default="E02", nargs="?")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--imgsz", type=int, default=None)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    exp = get_experiment(args.exp_id.upper())
    if exp.get("framework") != "ultralytics":
        raise SystemExit(f"{exp['id']} não pertence a YOLO_V8")

    epochs = args.epochs if args.epochs is not None else int(exp["epochs"])
    batch = args.batch if args.batch is not None else int(exp["batch"])
    imgsz = args.imgsz if args.imgsz is not None else int(exp["imgsz"])
    batch_cpu = int(exp.get("batch_cpu", 8))
    device_requested = args.device if args.device is not None else str(exp.get("device", "auto"))

    try:
        import torch
        import ultralytics

        device, device_msg = resolve_device(device_requested)
        batch = adjust_batch_for_device(batch, device, batch_cpu)
        print(f"[INFO] {device_msg}")

        log_lines = [
            f"exp_id={exp['id']}",
            f"framework=ultralytics",
            f"run_name={exp['run_name']}",
            f"data_yaml={exp['data_yaml']}",
            f"weights_init={exp['weights_init']}",
            f"epochs={epochs} batch={batch} imgsz={imgsz}",
            f"ultralytics={ultralytics.__version__}",
            f"torch={torch.__version__}",
            f"device={device}",
        ]
    except ImportError as err:
        raise SystemExit(
            "Ative venv_yolo_ultralytics:\n  .\\experiments\\YOLO_V8\\setup_venv_ultralytics.ps1"
        ) from err

    best_pt = train_ultralytics(exp, epochs, batch, imgsz, device)
    log_lines.append(f"best.pt={best_pt}")
    write_experiment_log(exp["output_dir"], log_lines)
    print(f"[OK] Treino concluído: {best_pt}")


if __name__ == "__main__":
    main()
