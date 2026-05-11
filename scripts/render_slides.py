from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def safe_survey_key(value: str) -> str:
    survey_key = value.strip()
    blocked = set('/\\:*?"<>|')
    if not survey_key or survey_key in {".", ".."} or any(ch in blocked for ch in survey_key):
        raise SystemExit("Survey key must be a simple folder-safe name.")
    return survey_key


def render_slides(survey_key: str, project_root: Path = PROJECT_ROOT) -> Path:
    survey_key = safe_survey_key(survey_key)
    quarto = shutil.which("quarto")
    if not quarto:
        raise SystemExit(
            "Quarto was not found on PATH. Install it from https://quarto.org/docs/download/ "
            "and verify with: quarto check"
        )

    input_file = project_root / "slides" / survey_key / "slides.qmd"
    if not input_file.exists():
        raise SystemExit(f"Slide file not found: {input_file}")

    output_dir = project_root / "build" / "slides" / survey_key
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        quarto,
        "render",
        str(input_file),
        "--output-dir",
        str(output_dir),
    ]
    result = subprocess.run(command, cwd=project_root, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    output_file = output_dir / "slides.html"
    if not output_file.exists():
        raise SystemExit(f"Expected rendered slides were not created: {output_file}")
    return output_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a survey Quarto slide deck.")
    parser.add_argument("--survey-key", default="repo_smoke_test")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_file = render_slides(args.survey_key)
    print(f"Rendered slides: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
