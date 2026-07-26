from __future__ import annotations

import argparse
import os
import sys

from .agent import synthesize
from .config import load_settings
from .manifest import build_manifest
from .retrieval import format_retrieval, retrieve


def _doctor() -> int:
    settings = load_settings()
    checks = {
        "python": sys.version.split()[0],
        "data_dir": str(settings.data_dir.resolve()),
        "snapshot_exists": settings.snapshot_dir.exists(),
        "manifest_exists": settings.manifest_path.exists(),
        "openai_key_present": bool(os.getenv("OPENAI_API_KEY")),
    }
    for key, value in checks.items():
        print(f"{key}: {value}")
    print("mode:", "openai-optional" if checks["openai_key_present"] else "retrieval-only")
    return 0


def _index() -> int:
    settings = load_settings()
    payload = build_manifest(settings.snapshot_dir, settings.manifest_path)
    print(f"Indexed {payload['file_count']} approved text files.")
    print(f"Manifest: {settings.manifest_path.resolve()}")
    return 0


def _ask(question: str, use_openai: bool) -> int:
    settings = load_settings()
    passages = retrieve(
        settings.snapshot_dir,
        question,
        max_results=settings.max_results,
        max_chars_per_result=settings.max_chars_per_result,
    )
    if use_openai:
        if not passages:
            print("No matching passages were found; OpenAI synthesis was not called.")
            return 2
        try:
            print(synthesize(question, passages, settings.openai_model))
            return 0
        except RuntimeError as exc:
            print(f"OpenAI synthesis unavailable: {exc}", file=sys.stderr)
            print("\nRetrieval fallback:\n")
            print(format_retrieval(passages))
            return 3
    print(format_retrieval(passages))
    return 0 if passages else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="captain-os", description="Read-only Captain OS bootstrap")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Show local configuration and capability mode.")
    commands.add_parser("index", help="Build a hash manifest of approved text sources.")
    ask = commands.add_parser("ask", help="Retrieve cited passages for a question.")
    ask.add_argument("question")
    ask.add_argument("--openai", action="store_true", help="Use optional OpenAI synthesis.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return _doctor()
    if args.command == "index":
        return _index()
    if args.command == "ask":
        return _ask(args.question, args.openai)
    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
