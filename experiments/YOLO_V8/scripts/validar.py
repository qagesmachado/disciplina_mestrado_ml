"""
Validação Ultralytics — E02 (venv_yolo_ultralytics).

Uso:
  python experiments/YOLO_V8/scripts/validar.py E02
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_SCRIPTS = SCRIPT_DIR.parent.parent / "shared" / "scripts"
for p in (str(SHARED_SCRIPTS), str(SCRIPT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from config_loader import get_experiment  # noqa: E402
from dataset_utils import load_val_image_paths  # noqa: E402
from device_utils import adjust_batch_for_device, resolve_device  # noqa: E402
from metrics_utils import f1_score, label_path_for_image, match_counts, read_yolo_file  # noqa: E402
from report_utils import write_html_report  # noqa: E402


def extract_ultralytics_metrics(metrics: object) -> tuple[float, float, float, float]:
    box = getattr(metrics, "box", None)
    if box is not None:
        return (
            float(getattr(box, "mp", 0.0) or 0.0),
            float(getattr(box, "mr", 0.0) or 0.0),
            float(getattr(box, "map50", 0.0) or 0.0),
            float(getattr(box, "map", 0.0) or 0.0),
        )
    return 0.0, 0.0, 0.0, 0.0


def run_ultralytics_val(
    model: object,
    data_yaml: Path,
    imgsz: int,
    batch: int,
    conf: float,
    device: str,
) -> tuple[tuple[float, float, float, float], float]:
    t0 = time.perf_counter()
    metrics = model.val(
        data=str(data_yaml),
        imgsz=imgsz,
        batch=batch,
        conf=conf,
        device=device,
        plots=False,
        verbose=False,
    )
    elapsed = time.perf_counter() - t0
    return extract_ultralytics_metrics(metrics), elapsed


def run_ultralytics_predict(
    model: object,
    image_paths: list[Path],
    detect_dir: Path,
    imgsz: int,
    conf: float,
    device: str,
) -> tuple[Path, float]:
    if not image_paths:
        raise ValueError("Lista de imagens vazia")

    list_file = detect_dir.parent / "_val_images_list.txt"
    list_file.write_text("\n".join(str(p) for p in image_paths), encoding="utf-8")

    t0 = time.perf_counter()
    model.predict(
        source=str(list_file),
        imgsz=imgsz,
        conf=conf,
        device=device,
        save_txt=True,
        save_conf=False,
        project=str(detect_dir.parent),
        name=detect_dir.name,
        exist_ok=True,
        verbose=False,
    )
    elapsed = time.perf_counter() - t0
    labels_dir = detect_dir / "labels"
    return (labels_dir if labels_dir.is_dir() else detect_dir), elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exp_id", default="E02", nargs="?")
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    exp = get_experiment(args.exp_id.upper())
    if exp.get("framework") != "ultralytics":
        raise SystemExit(f"{exp['id']} não pertence a YOLO_V8")

    exp_id = exp["id"]
    output_dir = exp["output_dir"]
    val_dir = output_dir / "val"
    val_dir.mkdir(parents=True, exist_ok=True)

    weights = args.weights.resolve() if args.weights else output_dir / "weights" / "best.pt"
    if not weights.is_file():
        raise FileNotFoundError(f"Pesos não encontrados: {weights}")

    data_yaml = exp["data_yaml"]
    conf = args.conf if args.conf is not None else float(exp["conf_thres"])
    imgsz = int(exp["imgsz"])
    batch = args.batch if args.batch is not None else int(exp.get("batch", 16))
    batch_cpu = int(exp.get("batch_cpu", 8))

    try:
        from ultralytics import YOLO
    except ImportError as err:
        raise SystemExit("Ative venv_yolo_ultralytics") from err

    device_requested = args.device if args.device is not None else str(exp.get("device", "auto"))
    device, device_msg = resolve_device(device_requested)
    batch = adjust_batch_for_device(batch, device, batch_cpu)
    print(f"[INFO] {device_msg}")

    model = YOLO(str(weights))
    t_total_start = time.perf_counter()

    (precision, recall, map50, map50_95), val_time_sec = run_ultralytics_val(
        model, data_yaml, imgsz, batch, conf, device
    )
    image_paths = load_val_image_paths(data_yaml)
    detect_labels, detect_time_sec = run_ultralytics_predict(
        model, image_paths, val_dir / "_detect_labels", imgsz, conf, device
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
        "framework": "ultralytics",
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
        script_label="experiments/YOLO_V8/scripts/validar.py",
    )
    print(f"[OK] {summary_csv}")
    print(f"[OK] Tempo total: {total_time_sec:.2f}s ({ms_per_image:.1f} ms/img)")


if __name__ == "__main__":
    main()
