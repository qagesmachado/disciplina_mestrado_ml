"""
Compatibilidade YOLOv5 (PyPI) com PyTorch >= 2.6 (weights_only) e NumPy/Pillow legados.
"""
from __future__ import annotations

import os


def apply_torch_load_patch() -> None:
    import torch

    if getattr(torch.load, "_tcd_patched", False):
        return

    _original_load = torch.load

    def _load_compat(*args, **kwargs):
        if "weights_only" not in kwargs:
            kwargs["weights_only"] = False
        return _original_load(*args, **kwargs)

    _load_compat._tcd_patched = True  # type: ignore[attr-defined]
    torch.load = _load_compat  # type: ignore[assignment]


def apply_numpy_pillow_patches() -> None:
    import numpy as np
    from PIL import ImageFont

    if not hasattr(np, "trapz") and hasattr(np, "trapezoid"):
        np.trapz = np.trapezoid  # type: ignore[attr-defined]

    if not hasattr(ImageFont.FreeTypeFont, "getsize"):
        def _compat_getsize(self, text):  # type: ignore[no-redef]
            left, top, right, bottom = self.getbbox(text)
            return right - left, bottom - top

        ImageFont.FreeTypeFont.getsize = _compat_getsize  # type: ignore[attr-defined]


def apply_all_yolov5_compat() -> None:
    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
    apply_torch_load_patch()
    apply_numpy_pillow_patches()
