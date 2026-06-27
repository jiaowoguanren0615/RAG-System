"""RAG evaluation runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def run_eval(dataset_path: Path) -> dict:
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    total = len(data)
    return {
        "total": total,
        "citation_accuracy": 0.0,
        "answer_accuracy": 0.0,
        "refusal_rate": 0.0,
        "version_accuracy": 0.0,
        "note": "Skeleton evaluator — implement scoring logic in P1.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RAG golden QA evaluation")
    parser.add_argument("--dataset", type=Path, default=Path("eval/golden_qa.json"))
    args = parser.parse_args()
    result = run_eval(args.dataset)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
