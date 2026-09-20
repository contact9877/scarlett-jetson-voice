from __future__ import annotations

from pathlib import Path
import re

ALLOWED_CONTINUATION_SUFFIXES = {".md", ".txt"}

RISK_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "authority_override",
        re.compile(
            r"\b(ignore|override|disregard|bypass)\b.{0,100}"
            r"\b(higher[- ]priority|system|developer|user|canonical|authority|policy)\b"
            r"|\b(treat|use)\b.{0,100}\b(summary|note|handoff|artifact|this)\b.{0,100}"
            r"\b(as|like)\b.{0,40}\b(standing\s+)?(authority|policy|canonical)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "concealment",
        re.compile(
            r"\b(do not|don't|never)\s+(disclose|mention|report|surface|reveal)\b"
            r"|\b(hide|conceal|suppress)\b.{0,80}\b(error|mismatch|failure|conflict|mistake)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "fabrication",
        re.compile(
            r"\b(invent|fabricate|make up|fill in)\b.{0,80}"
            r"\b(missing|history|fact|evidence|source|detail|data)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "permission_or_authority_escalation",
        re.compile(
            r"\b(grant|authorize|approve|enable|elevate|inherit)\b.{0,100}"
            r"\b(permission|authority|access|credential|deployment|write|control|admin|tool)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "persona_or_role_change",
        re.compile(
            r"\b(you are now|become|assume the role|new persona|replace your role)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "canonical_mutation_directive",
        re.compile(
            r"\b(delete|rewrite|overwrite|replace|modify|change)\b.{0,100}"
            r"\b(canonical|source of truth|authority|handoff|captain'?s log|crew context hub)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "credential_or_secret_request",
        re.compile(
            r"\b(password|passcode|api key|token|credential|secret)\b.{0,80}"
            r"\b(send|share|paste|expose|reveal|upload|store)\b"
            r"|\b(send|share|paste|expose|reveal|upload|store)\b.{0,80}"
            r"\b(password|passcode|api key|token|credential|secret)\b",
            re.IGNORECASE,
        ),
    ),
)

PROVENANCE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\s*(source|sources|provenance|canonical source)\s*:", re.IGNORECASE),
    re.compile(r"https://docs\.google\.com/", re.IGNORECASE),
    re.compile(r"https://drive\.google\.com/", re.IGNORECASE),
    re.compile(r"\bDrive ID\s*:", re.IGNORECASE),
    re.compile(r"\[[^\]]+#p\d+\]"),
)


def _matching_text(text: str, pattern: re.Pattern[str]) -> list[dict[str, object]]:
    """Return risk matches, including directives split across line boundaries.

    Replacing each newline with one space preserves string offsets, so a match can be
    mapped back to the originating line without retaining an absolute file path.
    """
    flattened = text.replace("\n", " ")
    matches: list[dict[str, object]] = []
    for match in pattern.finditer(flattened):
        line = text.count("\n", 0, match.start()) + 1
        snippet = " ".join(match.group(0).strip().split())
        matches.append({"line": line, "snippet": snippet[:240]})
    return matches


def inspect_continuation_text(text: str, *, source: str = "<memory>") -> dict[str, object]:
    findings: list[dict[str, object]] = []
    for category, pattern in RISK_PATTERNS:
        for item in _matching_text(text, pattern):
            findings.append({"category": category, **item})

    provenance_refs: list[dict[str, object]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in PROVENANCE_PATTERNS):
            snippet = " ".join(line.strip().split())
            provenance_refs.append({"line": number, "snippet": snippet[:240]})

    provenance_present = bool(provenance_refs)
    requires_human_review = bool(findings) or not provenance_present

    return {
        "schema_version": 1,
        "artifact_type": "derived_continuation",
        "source": source,
        "status": "REVIEW_REQUIRED" if requires_human_review else "DERIVED_CONTEXT_ONLY",
        "authority_effective": False,
        "canonical_write_authorized": False,
        "allowed_use": "context_only",
        "requires_canonical_reconciliation": True,
        "requires_human_review": requires_human_review,
        "provenance_present": provenance_present,
        "provenance_refs": provenance_refs,
        "findings": findings,
    }


def inspect_continuation_file(path: Path, *, max_file_bytes: int) -> dict[str, object]:
    if path.is_symlink():
        raise ValueError("Continuation artifact must not be a symbolic link.")
    if not path.exists() or not path.is_file():
        raise ValueError(f"Continuation artifact not found: {path}")
    if path.suffix.lower() not in ALLOWED_CONTINUATION_SUFFIXES:
        raise ValueError("Continuation artifact must be .md or .txt.")
    size = path.stat().st_size
    if size > max_file_bytes:
        raise ValueError(
            f"Continuation artifact exceeds the configured size limit ({size} > {max_file_bytes})."
        )
    text = path.read_text(encoding="utf-8", errors="replace")
    return inspect_continuation_text(text, source=path.name)
