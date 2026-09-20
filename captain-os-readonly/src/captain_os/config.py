from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from .sources import DEFAULT_MAX_FILE_BYTES


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    max_results: int
    max_chars_per_result: int
    max_file_bytes: int
    openai_model: str | None

    @property
    def snapshot_dir(self) -> Path:
        return self.data_dir / "approved_snapshot"

    @property
    def index_dir(self) -> Path:
        return self.data_dir / "index"

    @property
    def manifest_path(self) -> Path:
        return self.index_dir / "manifest.json"


def load_settings() -> Settings:
    return Settings(
        data_dir=Path(os.getenv("CAPTAIN_OS_DATA_DIR", "data")),
        max_results=max(1, int(os.getenv("CAPTAIN_OS_MAX_RESULTS", "5"))),
        max_chars_per_result=max(
            200, int(os.getenv("CAPTAIN_OS_MAX_CHARS_PER_RESULT", "1600"))
        ),
        max_file_bytes=max(
            1024, int(os.getenv("CAPTAIN_OS_MAX_FILE_BYTES", str(DEFAULT_MAX_FILE_BYTES)))
        ),
        openai_model=os.getenv("OPENAI_MODEL") or None,
    )
