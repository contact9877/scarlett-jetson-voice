from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ALLOWED_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True)
class ManifestEntry:
    relative_path: str
    sha256: str
    size_bytes: int
    modified_utc: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(snapshot_dir: Path, output_path: Path) -> dict[str, object]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    entries: list[ManifestEntry] = []

    for path in sorted(snapshot_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        stat = path.stat()
        entries.append(
            ManifestEntry(
                relative_path=path.relative_to(snapshot_dir).as_posix(),
                sha256=_sha256(path),
                size_bytes=stat.st_size,
                modified_utc=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            )
        )

    payload: dict[str, object] = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_root": str(snapshot_dir.resolve()),
        "file_count": len(entries),
        "entries": [asdict(entry) for entry in entries],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload
