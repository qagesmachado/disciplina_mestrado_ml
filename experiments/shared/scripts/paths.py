"""Caminhos compartilhados dos experimentos TCD."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS_ROOT = REPO_ROOT / "experiments"
YOLO_V5_ROOT = EXPERIMENTS_ROOT / "YOLO_V5"
YOLO_V8_ROOT = EXPERIMENTS_ROOT / "YOLO_V8"
YOLO_V11_ROOT = EXPERIMENTS_ROOT / "YOLO_V11"
SHARED_ROOT = EXPERIMENTS_ROOT / "shared"
SHARED_SCRIPTS = SHARED_ROOT / "scripts"
SHARED_OUTPUTS = SHARED_ROOT / "outputs"
PIG_ROOT = REPO_ROOT / "pig"
DATA_YAML_DIR = EXPERIMENTS_ROOT / "data" / "yaml"
DATA_YAML = DATA_YAML_DIR / "pig_dataset.yaml"
ENTREGA_TEMPLATES = REPO_ROOT / "entrega_parte_b_c" / "templates"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

ULTRALYTICS_V8_IDS = frozenset({"E02"})
ULTRALYTICS_V11_IDS = frozenset({"E03", "E04"})


def version_root_for_exp(exp_id: str) -> Path:
    exp_id = exp_id.upper()
    if exp_id in ULTRALYTICS_V11_IDS:
        return YOLO_V11_ROOT
    if exp_id in ULTRALYTICS_V8_IDS:
        return YOLO_V8_ROOT
    return YOLO_V5_ROOT


def config_filename_for_exp(exp_id: str) -> str:
    if version_root_for_exp(exp_id) == YOLO_V5_ROOT:
        return "experiments_yolov5.yaml"
    return "experiments.yaml"


def config_path_for_exp(exp_id: str) -> Path:
    return version_root_for_exp(exp_id) / "config" / config_filename_for_exp(exp_id)
