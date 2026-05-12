from __future__ import annotations

import argparse
import csv
import random
import sys
from pathlib import Path
from typing import Any

import qualtrics_workflow


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEXT_SNIPPETS = [
    "Clearer setup instructions",
    "Reusable prompts",
    "Example data",
    "More screenshots",
    "Simple install steps",
    "Document secrets setup",
]


def default_spec_path(survey_key: str, project_root: Path = PROJECT_ROOT) -> Path:
    return project_root / "code" / qualtrics_workflow.safe_survey_key(survey_key) / "survey_spec.json"


def default_output_path(survey_key: str, project_root: Path = PROJECT_ROOT) -> Path:
    return project_root / "tests" / "fixtures" / f"{qualtrics_workflow.safe_survey_key(survey_key)}_responses.csv"


def load_spec(spec_file: Path) -> dict[str, Any]:
    if not spec_file.exists():
        raise SystemExit(f"Survey spec not found: {spec_file}")
    return qualtrics_workflow.load_survey_spec(str(spec_file))


def answer_for_question(question: dict[str, Any], row_index: int, rng: random.Random) -> str:
    question_type = question["type"]
    if question_type == "mc":
        choices = [str(choice) for choice in question["choices"]]
        return choices[(row_index + rng.randrange(len(choices))) % len(choices)]
    if question_type == "text":
        return TEXT_SNIPPETS[(row_index + rng.randrange(len(TEXT_SNIPPETS))) % len(TEXT_SNIPPETS)]
    if question_type == "descriptive":
        return ""
    raise SystemExit(f"Unsupported question type for synthetic responses: {question_type}")


def response_rows(spec: dict[str, Any], n: int, seed: int) -> tuple[list[str], list[dict[str, str]]]:
    if n < 1:
        raise SystemExit("--n must be at least 1.")

    questions = [question for question in spec["questions"] if question["type"] != "descriptive"]
    headers = [str(question["tag"]) for question in questions]
    rng = random.Random(seed)
    rows: list[dict[str, str]] = []
    for row_index in range(n):
        rows.append(
            {
                str(question["tag"]): answer_for_question(question, row_index, rng)
                for question in questions
            }
        )
    return headers, rows


def write_csv(headers: list[str], rows: list[dict[str, str]], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def generate_synthetic_responses(
    survey_key: str,
    spec_file: Path | None = None,
    output_path: Path | None = None,
    n: int = 50,
    seed: int = 20260511,
    project_root: Path = PROJECT_ROOT,
) -> Path:
    survey_key = qualtrics_workflow.safe_survey_key(survey_key)
    spec_file = spec_file or default_spec_path(survey_key, project_root=project_root)
    output_path = output_path or default_output_path(survey_key, project_root=project_root)
    if not spec_file.is_absolute():
        spec_file = project_root / spec_file
    if not output_path.is_absolute():
        output_path = project_root / output_path

    spec = load_spec(spec_file)
    headers, rows = response_rows(spec, n=n, seed=seed)
    return write_csv(headers, rows, output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate local synthetic CSV responses from a survey spec.")
    parser.add_argument("--survey-key", default="repo_smoke_test")
    parser.add_argument("--spec-file", type=Path, help="Defaults to code/<survey_key>/survey_spec.json.")
    parser.add_argument("--output", type=Path, help="Defaults to tests/fixtures/<survey_key>_responses.csv.")
    parser.add_argument("--n", type=int, default=50, help="Number of synthetic responses to generate.")
    parser.add_argument("--seed", type=int, default=20260511, help="Random seed for deterministic output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_path = generate_synthetic_responses(
        args.survey_key,
        spec_file=args.spec_file,
        output_path=args.output,
        n=args.n,
        seed=args.seed,
    )
    print(f"Synthetic responses: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
