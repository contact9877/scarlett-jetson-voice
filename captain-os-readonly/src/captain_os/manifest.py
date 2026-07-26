from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from .sources import DEFAULT_MAX_FILE_BYTES, iter_approved_files


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


def _collect_entries(
    snapshot_dir: Path,
    *,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    for path in iter_approved_files(snapshot_dir, max_file_bytes=max_file_bytes):
        stat = path.stat()
        entries.append(
            ManifestEntry(
                relative_path=path.relative_to(snapshot_dir).as_posix(),
                sha256=_sha256(path),
                size_bytes=stat.st_size,
                modified_utc=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            )
        )
    return entries


def build_manifest(
    snapshot_dir: Path,
    output_path: Path,
    *,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
) -> dict[str, object]:
    entries = _collect_entries(snapshot_dir, max_file_bytes=max_file_bytes)
    payload: dict[str, object] = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_root": str(snapshot_dir.resolve()),
        "max_file_bytes": max_file_bytes,
        "file_count": len(entries),
        "entries": [asdict(entry) for entry in entries],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def load_manifest(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}. Run `captain-os index`.")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema.")
    return payload


def verify_manifest(
    snapshot_dir: Path,
    manifest_path: Path,
    *,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
) -> dict[str, object]:
    stored = load_manifest(manifest_path)
    stored_entries = {
        str(entry["relative_path"]): entry
        for entry in stored.get("entries", [])
        if isinstance(entry, dict) and "relative_path" in entry
    }
    current_entries = {
        entry.relative_path: asdict(entry)
        for entry in _collect_entries(snapshot_dir, max_file_bytes=max_file_bytes)
    }

    stored_paths = set(stored_entries)
    current_paths = set(current_entries)
    added = sorted(current_paths - stored_paths)
    removed = sorted(stored_paths - current_paths)
    changed = sorted(
        path
        for path in stored_paths & current_paths
        if stored_entries[path].get("sha256") != current_entries[path].get("sha256")
        or stored_entries[path].get("size_bytes") != current_entries[path].get("size_bytes")
    )
    unchanged = sorted((stored_paths & current_paths) - set(changed))

    return {
        "ok": not added and not removed and not changed,
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged_count": len(unchanged),
        "stored_file_count": len(stored_entries),
        "current_file_count": len(current_entries),
    }
