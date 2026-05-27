"""
Validação YOLOv5 — E01 e REF (venv_yolo_5).

Uso:
  python experiments/YOLO_V5/scripts/validar.py E01
  python experiments/YOLO_V5/scripts/validar.py REF
"""
from __future__ import annotations

import argparse
import csv
import inspect
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_SCRIPTS = SCRIPT_DIR.parent.parent / "shared" / "scripts"
for p in (str(SHARED_SCRIPTS), str(SCRIPT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from config_loader import get_experiment, resolve_weights  # noqa: E402
from dataset_utils import load_val_image_paths  # noqa: E402
from device_utils import adjust_batch_for_device, resolve_device  # noqa: E402
from metrics_utils import extract_main_metrics, f1_score, label_path_for_image, match_counts, read_yolo_file  # noqa: E402
from paths import REPO_ROOT  # noqa: E402
from report_utils import write_html_report  # noqa: E402


def apply_yolov5_compat_patches() -> None:
    from yolov5_compat import apply_all_yolov5_compat

    apply_all_yolov5_compat()


def run_validation(
    weights: Path,
    data_yaml: Path,
    output_val_dir: Path,
    imgsz: int,
    batch: int,
    conf: float,
    device: str,
) -> tuple[tuple[float, float, float, float], float]:
    apply_yolov5_compat_patches()
    from yolov5.val import run as val_run

    requested = {
        "data": str(data_yaml),
        "weights": str(weights),
        "imgsz": imgsz,
        "batch_size": batch,
        "project": str(output_val_dir.parent),
        "name": output_val_dir.name,
        "exist_ok": True,
        "save_txt": True,
        "save_json": False,
        "verbose": False,
        "conf_thres": conf,
        "device": device,
    }
    valid_params = set(inspect.signature(val_run).parameters.keys())
    filtered = {k: v for k, v in requested.items() if k in valid_params}
    if "plots" in valid_params:
        filtered["plots"] = False
    if "device" not in valid_params:
        filtered.pop("device", None)

    print("[INFO] yolov5.val:", filtered)
    t0 = time.perf_counter()
    result = val_run(**filtered)
    elapsed = time.perf_counter() - t0
    return extract_main_metrics(result), elapsed


def run_detect_for_per_image(
    weights: Path,
    image_paths: list[Path],
    detect_dir: Path,
    imgsz: int,
    conf: float,
    device: str,
) -> tuple[Path, float]:
    if not image_paths:
        raise ValueError("Lista de imagens de validação vazia")

    list_file = detect_dir.parent / "_val_images_list.txt"
    list_file.write_text("\n".join(str(p) for p in image_paths), encoding="utf-8")

    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_yolov5_cli.py"),
        "detect",
        "--weights",
        str(weights),
        "--source",
        str(list_file),
        "--img",
        str(imgsz),
        "--conf",
        str(conf),
        "--project",
        str(detect_dir.parent),
        "--name",
        detect_dir.name,
        "--exist-ok",
        "--save-txt",
        "--device",
        device,
    ]
    print("[INFO] yolov5.detect:", " ".join(cmd))
    t0 = time.perf_counter()
    subprocess.run(cmd, check=True, cwd=str(REPO_ROOT), env=os.environ.copy())
    elapsed = time.perf_counter() - t0
    return detect_dir / "labels", elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exp_id")
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    exp = get_experiment(args.exp_id.upper())
    exp_id = exp["id"]
    if exp.get("framework") != "yolov5":
        raise SystemExit(f"{exp_id} não pertence a YOLO_V5")

    output_dir = exp["output_dir"]
    val_dir = output_dir / "val"
    val_dir.mkdir(parents=True, exist_ok=True)

    if args.weights:
        weights = args.weights.resolve()
    elif exp_id == "REF":
        weights = resolve_weights("pig/best.pt")
    else:
        weights = output_dir / "weights" / "best.pt"

    if not weights.is_file():
        raise FileNotFoundError(f"Pesos não encontrados: {weights}")

    data_yaml = exp["data_yaml"]
    conf = args.conf if args.conf is not None else float(exp["conf_thres"])
    imgsz = int(exp["imgsz"])
    batch = args.batch if args.batch is not None else int(exp.get("batch", 16))
    batch_cpu = int(exp.get("batch_cpu", 8))

    try:
        import yolov5  # noqa: F401
    except ImportError as err:
        raise SystemExit("Ative venv_yolo_5 e instale requirements-yolov5.txt") from err

    device_requested = args.device if args.device is not None else str(exp.get("device", "auto"))
    device, device_msg = resolve_device(device_requested)
    batch = adjust_batch_for_device(batch, device, batch_cpu)
    print(f"[INFO] {device_msg}")

    t_total_start = time.perf_counter()
    (precision, recall, map50, map50_95), val_time_sec = run_validation(
        weights, data_yaml, val_dir / "_yolov5_val_run", imgsz, batch, conf, device
    )
    image_paths = load_val_image_paths(data_yaml)
    detect_labels, detect_time_sec = run_detect_for_per_image(
        weights, image_paths, val_dir / "_detect_labels", imgsz, conf, device
    )

    t_match_start = time.perf_counter()
    per_image_rows: list[dict[str, object]] = []
    for image_path in image_paths:
        gt = read_yolo_file(label_path_for_image(image_path))
        pred = read_yolo_file(detect_labels / f"{image_path.stem}.txt")
        tp, fp, fn = match_counts(gt, pred, iou_threshold=0.5)
        per_image_rows.append(
            {
                "image_name": image_path.name,
                "ground_truth_count": len(gt),
                "predicted_count": len(pred),
                "true_positives": tp,
                "false_positives": fp,
                "false_negatives": fn,
                "counting_error": abs(len(pred) - len(gt)),
            }
        )
    match_time_sec = time.perf_counter() - t_match_start
    total_time_sec = time.perf_counter() - t_total_start
    n_images = len(image_paths)
    ms_per_image = (total_time_sec / n_images * 1000.0) if n_images else 0.0
    f1 = f1_score(precision, recall)

    summary = {
        "experimento": exp_id,
        "modelo": exp.get("model_label", ""),
        "split": exp["split_code"],
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "map50": round(map50, 6),
        "map50_95": round(map50_95, 6),
        "f1": round(f1, 6),
        "n_val_images": n_images,
        "val_time_sec": round(val_time_sec, 3),
        "detect_time_sec": round(detect_time_sec, 3),
        "match_time_sec": round(match_time_sec, 3),
        "total_time_sec": round(total_time_sec, 3),
        "ms_per_image": round(ms_per_image, 2),
        "device": device,
        "weights": str(weights),
        "data_yaml": str(data_yaml),
        "conf_thres": conf,
        "framework": "yolov5",
    }

    per_image_csv = val_dir / "per_image_tp_fp_fn.csv"
    summary_csv = val_dir / "metrics_summary.csv"
    with per_image_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "image_name",
                "ground_truth_count",
                "predicted_count",
                "true_positives",
                "false_positives",
                "false_negatives",
                "counting_error",
            ],
        )
        w.writeheader()
        w.writerows(per_image_rows)
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary.keys()))
        w.writeheader()
        w.writerow(summary)

    write_html_report(
        val_dir,
        exp_id,
        summary,
        per_image_csv,
        summary_csv,
        script_label="experiments/YOLO_V5/scripts/validar.py",
    )
    print(f"[OK] {summary_csv}")
    print(f"[OK] Tempo total: {total_time_sec:.2f}s ({ms_per_image:.1f} ms/img)")


if __name__ == "__main__":
    main()
