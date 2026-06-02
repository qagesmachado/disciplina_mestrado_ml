"""Carrega config de experiments/YOLO_V5|YOLO_V8|YOLO_V11 (experiments_yolov5.yaml ou experiments.yaml)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from paths import DATA_YAML, REPO_ROOT, SHARED_OUTPUTS, config_path_for_exp, version_root_for_exp


def load_config(exp_id: str) -> dict[str, Any]:
    path = config_path_for_exp(exp_id)
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_experiment(exp_id: str) -> dict[str, Any]:
    exp_id = exp_id.upper()
    cfg = load_config(exp_id)
    exp = cfg.get("experiments", {}).get(exp_id)
    if not exp:
        raise KeyError(f"Experimento desconhecido em {version_root_for_exp(exp_id)}: {exp_id}")
    defaults = cfg.get("defaults", {})
    version_root = version_root_for_exp(exp_id)
    data_yaml = DATA_YAML.resolve()
    return {
        "id": exp_id,
        **defaults,
        **exp,
        "split_code": cfg["dataset"]["name"],
        "data_yaml": data_yaml,
        "output_dir": (version_root / "outputs" / exp["run_name"]).resolve(),
        "version_root": version_root,
    }


def resolve_weights(weights: str) -> Path:
    p = Path(weights)
    if p.is_file():
        return p.resolve()
    candidate = REPO_ROOT / weights
    if candidate.is_file():
        return candidate.resolve()
    return p


def comparison_outputs_dir() -> Path:
    SHARED_OUTPUTS.mkdir(parents=True, exist_ok=True)
    return SHARED_OUTPUTS
