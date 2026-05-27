"""
Garante YAML do dataset pig (train/val fixos do Kaggle).

Uso:
  python experiments/shared/scripts/ensure_pig_dataset.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from paths import DATA_YAML, EXPERIMENTS_ROOT, PIG_ROOT, REPO_ROOT  # noqa: E402

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def count_images(folder: Path) -> int:
    if not folder.is_dir():
        return 0
    return sum(1 for p in folder.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)


def main() -> None:
    train_dir = PIG_ROOT / "train" / "images"
    val_dir = PIG_ROOT / "val" / "images"
    if not train_dir.is_dir() or not val_dir.is_dir():
        raise FileNotFoundError(
            f"Estrutura pig/ esperada: train/images e val/images em {PIG_ROOT}"
        )

    n_train = count_images(train_dir)
    n_val = count_images(val_dir)

    DATA_YAML.parent.mkdir(parents=True, exist_ok=True)
    DATA_YAML.write_text(
        f"path: {repr(str(PIG_ROOT.resolve()))}\n"
        "train: train/images\n"
        "val: val/images\n"
        "nc: 1\n"
        "names:\n"
        "  0: pig\n",
        encoding="utf-8",
    )

    manifest = {
        "dataset": "pig_kaggle",
        "path": str(PIG_ROOT.resolve()),
        "train_images": n_train,
        "val_images": n_val,
        "total": n_train + n_val,
        "data_yaml": str(DATA_YAML.resolve()),
        "note": "Particao fixa original do repositorio",
    }
    manifest_path = EXPERIMENTS_ROOT / "data" / "pig_dataset_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"[OK] train={n_train} val={n_val} total={n_train + n_val}")
    print(f"[OK] YAML: {DATA_YAML.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
