from __future__ import annotations

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).parents[1]

TEXT_SUFFIXES = {
    ".cfg",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

FORBIDDEN_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "environment_report.json",
    "id_ed25519",
    "id_rsa",
}

FORBIDDEN_SECRET_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "github_pat",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "aws_access_key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "slack_token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    ),
    (
        "openai_key",
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    ),
)


def _project_files() -> list[Path]:
    return [
        path
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


def test_sensitive_local_artifacts_are_not_present() -> None:
    findings: list[str] = []
    for path in _project_files():
        if path.name in FORBIDDEN_FILENAMES or path.suffix.lower() in FORBIDDEN_SECRET_SUFFIXES:
            findings.append(str(path.relative_to(PROJECT_ROOT)))
    assert findings == []


def test_obvious_real_secret_patterns_are_absent() -> None:
    findings: list[str] = []
    for path in _project_files():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.stat().st_size > 2 * 1024 * 1024:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"{path.relative_to(PROJECT_ROOT)}:{label}")
    assert findings == []


def test_environment_inventory_output_is_gitignored() -> None:
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "environment_report.json" in {line.strip() for line in gitignore}


def test_environment_collector_does_not_log_absolute_output_path() -> None:
    source = (PROJECT_ROOT / "scripts" / "collect_environment.py").read_text(encoding="utf-8")
    assert "output.resolve()" not in source
    assert 'output.name' in source
