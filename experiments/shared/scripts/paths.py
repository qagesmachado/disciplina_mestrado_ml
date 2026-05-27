"""Caminhos compartilhados dos experimentos TCD."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS_ROOT = REPO_ROOT / "experiments"
YOLO_V5_ROOT = EXPERIMENTS_ROOT / "YOLO_V5"
YOLO_V8_ROOT = EXPERIMENTS_ROOT / "YOLO_V8"
SHARED_ROOT = EXPERIMENTS_ROOT / "shared"
SHARED_SCRIPTS = SHARED_ROOT / "scripts"
SHARED_OUTPUTS = SHARED_ROOT / "outputs"
PIG_ROOT = REPO_ROOT / "pig"
DATA_YAML_DIR = EXPERIMENTS_ROOT / "data" / "yaml"
DATA_YAML = DATA_YAML_DIR / "pig_dataset.yaml"
ENTREGA_TEMPLATES = REPO_ROOT / "entrega_parte_b_c" / "templates"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

ULTRALYTICS_EXP_IDS = frozenset({"E02", "E03", "E04"})


def version_root_for_exp(exp_id: str) -> Path:
    if exp_id.upper() in ULTRALYTICS_EXP_IDS:
        return YOLO_V8_ROOT
    return YOLO_V5_ROOT


def config_path_for_exp(exp_id: str) -> Path:
    return version_root_for_exp(exp_id) / "config" / "experiments.yaml"
