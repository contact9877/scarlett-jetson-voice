from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def safe_command(command: list[str], timeout: int = 8) -> str | None:
    executable = shutil.which(command[0])
    if not executable:
        return None
    try:
        result = subprocess.run(
            [executable, *command[1:]],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (result.stdout or result.stderr).strip()
    return output[:4000] if output else None


def disk_summary(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    usage = shutil.disk_usage(path)
    gib = 1024**3
    return {
        "path": str(path),
        "total_gib": round(usage.total / gib, 2),
        "used_gib": round(usage.used / gib, 2),
        "free_gib": round(usage.free / gib, 2),
    }


def physical_memory_gib() -> float | None:
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                if line.startswith("MemTotal:"):
                    kib = int(line.split()[1])
                    return round(kib / 1024 / 1024, 2)
        except (OSError, ValueError):
            return None
    if sys.platform == "win32":
        value = safe_command([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
        ])
        try:
            return round(int(value or "0") / 1024**3, 2) or None
        except ValueError:
            return None
    return None


def main() -> int:
    # Deliberately excludes usernames, hostnames, Wi-Fi names, IP addresses,
    # environment variables, tokens, file listings, and document contents.
    roots = [Path.cwd().anchor or "/"]
    if sys.platform == "win32":
        roots = [Path("C:/"), Path("D:/")]

    report = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_note": "No credentials, network identifiers, usernames, or file contents collected.",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or None,
            "python": platform.python_version(),
        },
        "cpu_logical_count": os.cpu_count(),
        "physical_memory_gib": physical_memory_gib(),
        "disks": [item for item in (disk_summary(path) for path in roots) if item],
        "tool_versions": {
            "git": safe_command(["git", "--version"]),
            "docker": safe_command(["docker", "--version"]),
            "docker_compose": safe_command(["docker", "compose", "version"]),
            "nvidia_smi": safe_command([
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader",
            ]),
        },
    }

    output = Path("environment_report.json")
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote non-secret environment inventory: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
