"""Detecção de GPU/CPU para treino e validação."""
from __future__ import annotations


def resolve_device(requested: str | None = "auto") -> tuple[str, str]:
    import torch

    req = (requested or "auto").strip().lower()

    if req in ("auto", "", "default"):
        if torch.cuda.is_available():
            return "0", "GPU CUDA detectada — usando device 0"
        return "cpu", "CUDA não disponível — usando CPU (treino mais lento)"

    if req == "cpu":
        return "cpu", "CPU (informado explicitamente)"

    wants_gpu = req.isdigit() or req.startswith("cuda") or "," in req
    if wants_gpu and not torch.cuda.is_available():
        return (
            "cpu",
            f"Pedido device={requested!r}, mas PyTorch não vê CUDA "
            f"(torch {torch.__version__}). Usando CPU.",
        )

    if req.startswith("cuda:"):
        return req.split(":", 1)[1], f"GPU {req}"
    return requested or "cpu", f"device={requested}"


def adjust_batch_for_device(batch: int, device: str, batch_cpu: int = 8) -> int:
    if device == "cpu" and batch > batch_cpu:
        return batch_cpu
    return batch


def adjust_workers_for_device(workers: int, device: str) -> int:
    if device == "cpu":
        return min(workers, 0)
    return workers
