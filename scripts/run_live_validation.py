from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


@dataclass(frozen=True)
class ValidationStep:
    name: str
    argv: list[str]
    display_argv: list[str]


def safe_survey_key(survey_key: str) -> str:
    value = survey_key.strip()
    blocked = set('/\\:*?"<>|')
    if not value or value in {".", ".."} or any(ch in blocked for ch in value):
        raise SystemExit("Survey key must be a simple folder-safe name.")
    return value


def rel_display(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        return str(path)
    return str(relative).replace("/", "\\")


def command_text(argv: list[str]) -> str:
    return subprocess.list2cmdline(argv)


def python_step(script: Path, args: list[str]) -> tuple[list[str], list[str]]:
    return [sys.executable, str(script), *args], ["python", rel_display(script), *args]


def build_steps(args: argparse.Namespace) -> list[ValidationStep]:
    survey_key = safe_survey_key(args.survey_key)
    spec_file = Path(args.spec_file)
    spec_display = args.spec_file
    if not spec_file.is_absolute():
        spec_file = PROJECT_ROOT / spec_file
    if not spec_file.exists() and not args.dry_run:
        raise SystemExit(f"Survey spec not found: {spec_file}")

    fixture = Path(args.synthetic_output or f"build/fixtures/{survey_key}_responses.csv")
    fixture_display = str(fixture)
    qwf = PROJECT_ROOT / "scripts" / "qualtrics_workflow.py"
    generator = PROJECT_ROOT / "scripts" / "generate_synthetic_responses.py"
    analysis = PROJECT_ROOT / "scripts" / "run_analysis.py"
    slides = PROJECT_ROOT / "scripts" / "build_slides.py"

    steps: list[ValidationStep] = []

    def add(name: str, script: Path, step_args: list[str]) -> None:
        argv, display = python_step(script, step_args)
        steps.append(ValidationStep(name, argv, display))

    add("check-auth", qwf, ["check-auth"])
    add(
        "create-survey",
        qwf,
        [
            "create-survey",
            "--survey-name",
            args.survey_name,
            "--survey-key",
            survey_key,
            "--spec-file",
            spec_display,
        ],
    )

    link_args = ["get-link", "--survey-key", survey_key, "--survey-name", args.survey_name, "--write-slide-inputs"]
    if args.public_host:
        link_args.extend(["--public-host", args.public_host])
    add("get-private-link", qwf, link_args)

    add(
        "prepare-synthetic-rows",
        generator,
        ["--survey-key", survey_key, "--spec-file", spec_display, "--output", fixture_display, "--n", str(args.n)],
    )
    add(
        "submit-synthetic-responses",
        qwf,
        [
            "submit-synthetic-responses",
            "--survey-key",
            survey_key,
            "--survey-name",
            args.survey_name,
            "--spec-file",
            spec_display,
            "--input",
            fixture_display,
        ],
    )
    add(
        "export-responses",
        qwf,
        ["export-responses", "--survey-key", survey_key, "--survey-name", args.survey_name, "--format", args.export_format],
    )
    add("analyze-responses", analysis, ["--survey-key", survey_key])
    add("build-beamer-or-fallback-slides", slides, ["--survey-key", survey_key, "--mode", "auto"])

    return steps


def summary_payload(args: argparse.Namespace, steps: list[dict[str, Any]], status: str) -> dict[str, Any]:
    return {
        "survey_key": safe_survey_key(args.survey_key),
        "survey_name": args.survey_name,
        "spec_file": args.spec_file,
        "requested_synthetic_responses": args.n,
        "export_format": args.export_format,
        "dry_run": bool(args.dry_run),
        "status": status,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "steps": steps,
        "notes": [
            "Command output is streamed to the local terminal for teaching but is not stored here.",
            "Survey IDs, response IDs, reusable links, tokens, Qualtrics URLs, raw rows, and metadata contents are not stored here.",
        ],
    }


def write_summary(args: argparse.Namespace, steps: list[dict[str, Any]], status: str) -> Path:
    survey_key = safe_survey_key(args.survey_key)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = DATA_DIR / survey_key / "metadata" / f"live_validation_summary_{timestamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary_payload(args, steps, status), indent=2) + "\n", encoding="utf-8")
    return path


def run_step(step: ValidationStep) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(step.argv, cwd=PROJECT_ROOT, text=True, check=False)
    elapsed = round(time.monotonic() - started, 3)
    return {
        "name": step.name,
        "command": command_text(step.display_argv),
        "exit_code": completed.returncode,
        "duration_seconds": elapsed,
        "status": "ok" if completed.returncode == 0 else "failed",
    }


def command_dry_run(steps: list[ValidationStep]) -> int:
    print("Dry run only. No Qualtrics API calls, response exports, analysis, or slide builds were executed.")
    for index, step in enumerate(steps, start=1):
        print(f"{index}. {step.name}: {command_text(step.display_argv)}")
    return 0


def command_run(args: argparse.Namespace, steps: list[ValidationStep]) -> int:
    executed_steps: list[dict[str, Any]] = []
    for index, step in enumerate(steps, start=1):
        print(f"Running {index}/{len(steps)}: {step.name}")
        result = run_step(step)
        executed_steps.append(result)
        if result["status"] != "ok":
            summary_path = write_summary(args, executed_steps, "failed")
            print(f"Step failed: {step.name}")
            print("Review the command output above, then rerun the failed step after fixing the issue.")
            print(f"Wrote sanitized validation summary: {summary_path}")
            return int(result["exit_code"]) or 1

    summary_path = write_summary(args, executed_steps, "completed")
    print(f"Wrote sanitized validation summary: {summary_path}")
    print("Live validation completed. Archive or delete the local Qualtrics test survey manually if it is no longer needed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the lean local live Qualtrics demo loop.")
    parser.add_argument("--survey-key", required=True)
    parser.add_argument("--survey-name", required=True)
    parser.add_argument("--spec-file", required=True)
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--synthetic-output", help="Defaults to build/fixtures/<survey_key>_responses.csv.")
    parser.add_argument("--export-format", choices=["csv", "spss"], default="csv", help="Use csv for Python-first validation or spss for Stata/SAV validation.")
    parser.add_argument("--public-host", help="Respondent-facing Qualtrics host for reusable links.")
    parser.add_argument("--dry-run", action="store_true", help="Print the command sequence without running it.")
    parser.add_argument(
        "--i-understand-this-calls-qualtrics",
        action="store_true",
        help="Accepted for compatibility; live API intent is implied by running this helper without --dry-run.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.n < 1:
        parser.error("--n must be at least 1.")

    steps = build_steps(args)
    if args.dry_run:
        return command_dry_run(steps)
    return command_run(args, steps)


if __name__ == "__main__":
    sys.exit(main())
