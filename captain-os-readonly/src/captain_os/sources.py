from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

ALLOWED_SUFFIXES = {".md", ".txt"}
DEFAULT_MAX_FILE_BYTES = 2 * 1024 * 1024


def iter_approved_files(
    snapshot_dir: Path,
    *,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
) -> Iterator[Path]:
    """Yield regular approved text files that remain inside the snapshot root.

    Symbolic links are rejected even when they point back inside the root. This keeps the
    snapshot boundary explicit and prevents an approved directory from becoming an
    indirect path into unrelated local files.
    """
    root = snapshot_dir.resolve()
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(snapshot_dir.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue

        try:
            resolved = path.resolve(strict=True)
            size = path.stat().st_size
        except OSError:
            continue

        if not resolved.is_relative_to(root):
            continue
        if size > max_file_bytes:
            continue
        yield path
