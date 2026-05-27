"""Log de experimento em output_dir/experiment_log.txt."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def write_experiment_log(output_dir: Path, lines: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "experiment_log.txt"
    header = f"# {datetime.now(timezone.utc).isoformat()}\n"
    log_path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
