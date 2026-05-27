"""Utilitários de métricas (reutilizados na validação)."""
from __future__ import annotations

from pathlib import Path

import numpy as np


def read_yolo_file(path: Path) -> list[tuple[int, float, float, float, float]]:
    rows: list[tuple[int, float, float, float, float]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        rows.append(
            (
                int(float(parts[0])),
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
                float(parts[4]),
            )
        )
    return rows


def yolo_to_xyxy(x_center: float, y_center: float, width: float, height: float) -> tuple[float, float, float, float]:
    x1 = x_center - width / 2
    y1 = y_center - height / 2
    x2 = x_center + width / 2
    y2 = y_center + height / 2
    return x1, y1, x2, y2


def iou(box_a: tuple[float, float, float, float], box_b: tuple[float, float, float, float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter_area
    if union <= 0:
        return 0.0
    return inter_area / union


def match_counts(
    ground_truth_rows: list[tuple[int, float, float, float, float]],
    prediction_rows: list[tuple[int, float, float, float, float]],
    iou_threshold: float = 0.5,
) -> tuple[int, int, int]:
    used_ground_truth = [False] * len(ground_truth_rows)
    true_positives = 0
    false_positives = 0

    for prediction in prediction_rows:
        prediction_class, px, py, pw, ph = prediction
        prediction_box = yolo_to_xyxy(px, py, pw, ph)
        best_iou = 0.0
        best_index = -1
        for index, ground_truth in enumerate(ground_truth_rows):
            if used_ground_truth[index]:
                continue
            ground_truth_class, gx, gy, gw, gh = ground_truth
            if prediction_class != ground_truth_class:
                continue
            current_iou = iou(prediction_box, yolo_to_xyxy(gx, gy, gw, gh))
            if current_iou > best_iou:
                best_iou = current_iou
                best_index = index

        if best_index >= 0 and best_iou >= iou_threshold:
            used_ground_truth[best_index] = True
            true_positives += 1
        else:
            false_positives += 1

    false_negatives = used_ground_truth.count(False)
    return true_positives, false_positives, false_negatives


def extract_main_metrics(val_result: object) -> tuple[float, float, float, float]:
    def _flatten_numbers(value: object) -> list[float]:
        numbers: list[float] = []
        if isinstance(value, (int, float)):
            numbers.append(float(value))
        elif isinstance(value, np.ndarray):
            try:
                numbers.extend([float(v) for v in value.flatten().tolist()])
            except Exception:
                pass
        elif isinstance(value, (list, tuple)):
            for item in value:
                numbers.extend(_flatten_numbers(item))
        return numbers

    if isinstance(val_result, dict):
        precision = float(val_result.get("mp", 0.0))
        recall = float(val_result.get("mr", 0.0))
        map_50 = float(val_result.get("map50", 0.0))
        map_50_95 = float(val_result.get("map", 0.0))
        return precision, recall, map_50, map_50_95

    flattened = _flatten_numbers(val_result)
    if len(flattened) >= 4:
        return flattened[0], flattened[1], flattened[2], flattened[3]

    return 0.0, 0.0, 0.0, 0.0


def f1_score(precision: float, recall: float) -> float:
    if precision + recall <= 0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


def label_path_for_image(image_path: Path) -> Path:
    parts = list(image_path.parts)
    if "images" not in parts:
        raise ValueError(f"Caminho de imagem fora do padrão YOLO: {image_path}")
    idx = parts.index("images")
    parts[idx] = "labels"
    return Path(*parts[:-1]) / f"{image_path.stem}.txt"
