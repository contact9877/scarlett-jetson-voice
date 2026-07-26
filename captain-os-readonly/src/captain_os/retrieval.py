from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_'’-]*")
PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")


@dataclass(frozen=True)
class Passage:
    source: str
    ordinal: int
    text: str
    score: float

    @property
    def citation(self) -> str:
        return f"{self.source}#p{self.ordinal}"


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if len(token) > 1}


def retrieve(
    snapshot_dir: Path,
    query: str,
    *,
    max_results: int = 5,
    max_chars_per_result: int = 1600,
) -> list[Passage]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    candidates: list[Passage] = []
    for path in sorted(snapshot_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(snapshot_dir).as_posix()

        ordinal = 0
        for raw in PARAGRAPH_SPLIT_RE.split(text):
            paragraph = " ".join(raw.split()).strip()
            if not paragraph:
                continue
            ordinal += 1
            paragraph_tokens = _tokens(paragraph)
            overlap = query_tokens & paragraph_tokens
            if not overlap:
                continue
            coverage = len(overlap) / len(query_tokens)
            density = len(overlap) / max(1, len(paragraph_tokens))
            exact_bonus = 0.25 if query.lower() in paragraph.lower() else 0.0
            candidates.append(
                Passage(
                    source=relative,
                    ordinal=ordinal,
                    text=paragraph[:max_chars_per_result],
                    score=round(coverage * 0.75 + density * 0.25 + exact_bonus, 6),
                )
            )

    candidates.sort(key=lambda item: (-item.score, item.source, item.ordinal))
    return candidates[:max_results]


def format_retrieval(passages: list[Passage]) -> str:
    if not passages:
        return "No matching passages were found in the approved snapshot."
    return "\n\n".join(
        f"[{passage.citation}] score={passage.score:.3f}\n{passage.text}"
        for passage in passages
    )
