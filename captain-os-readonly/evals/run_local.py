from __future__ import annotations

import json
from pathlib import Path
import tempfile

from captain_os.retrieval import retrieve


def run_case(case: dict[str, object]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="captain-os-eval-") as temp:
        root = Path(temp)
        documents = case.get("documents", {})
        assert isinstance(documents, dict)
        for name, content in documents.items():
            (root / str(name)).write_text(str(content), encoding="utf-8")

        results = retrieve(root, str(case["question"]), max_results=5)
        expect_match = bool(case.get("expect_match", True))
        passed = bool(results) == expect_match
        reasons: list[str] = []

        if expect_match and results:
            expected_contains = case.get("expected_contains")
            expected_source = case.get("expected_source")
            joined = "\n".join(item.text for item in results)
            sources = {item.source for item in results}
            citations = [item.citation for item in results]

            if expected_contains and str(expected_contains) not in joined:
                passed = False
                reasons.append(f"missing expected text: {expected_contains}")
            if expected_source and str(expected_source) not in sources:
                passed = False
                reasons.append(f"missing expected source: {expected_source}")
            if not all("#p" in citation for citation in citations):
                passed = False
                reasons.append("one or more results lacked paragraph citations")

        if not expect_match and results:
            reasons.append("unexpected retrieval match")

        return {
            "name": case["name"],
            "passed": passed,
            "result_count": len(results),
            "citations": [item.citation for item in results],
            "reasons": reasons,
        }


def main() -> int:
    cases_path = Path(__file__).with_name("cases.jsonl")
    cases = [
        json.loads(line)
        for line in cases_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    results = [run_case(case) for case in cases]
    output_dir = Path(__file__).with_name("results")
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "latest.json"
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    failed = [result for result in results if not result["passed"]]
    print(json.dumps(results, indent=2))
    print(f"Evaluation results: {len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
