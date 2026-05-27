"""Utilitários de dataset YOLO compartilhados (YOLOv5 e Ultralytics)."""
from __future__ import annotations

from pathlib import Path

from paths import IMAGE_SUFFIXES, REPO_ROOT


def read_yaml_field(yaml_path: Path, key: str) -> str:
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            return stripped.split(":", 1)[1].strip().strip("'\"")
    raise KeyError(f"Campo '{key}' não encontrado em {yaml_path}")


def resolve_dataset_split_path(data_yaml: Path, field: str) -> Path:
    split_field = read_yaml_field(data_yaml, field)
    split_path = Path(split_field)

    if split_path.is_absolute():
        return split_path.resolve()

    if split_path.suffix.lower() == ".txt":
        if not split_path.is_file():
            split_path = (REPO_ROOT / split_field).resolve()
        return split_path

    try:
        dataset_root = Path(read_yaml_field(data_yaml, "path")).resolve()
    except KeyError:
        dataset_root = data_yaml.parent

    if not dataset_root.is_absolute():
        dataset_root = (REPO_ROOT / dataset_root).resolve()

    return (dataset_root / split_field).resolve()


def load_val_image_paths(data_yaml: Path) -> list[Path]:
    val_path = resolve_dataset_split_path(data_yaml, "val")

    if val_path.suffix.lower() == ".txt":
        lines = [ln.strip() for ln in val_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        return [Path(ln).resolve() for ln in lines]

    if val_path.is_dir():
        return sorted(
            p.resolve()
            for p in val_path.iterdir()
            if p.suffix.lower() in IMAGE_SUFFIXES
        )

    raise ValueError(f"val não encontrado ou formato inválido: {val_path}")
