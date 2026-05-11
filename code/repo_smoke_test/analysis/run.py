from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator


SURVEY_KEY = "repo_smoke_test"
PROJECT_ROOT = Path(__file__).resolve().parents[3]

VARIABLES = {
    "role": ["Student", "Instructor", "Researcher", "Administrator", "Other"],
    "workflow_familiarity": [
        "Not familiar",
        "Slightly familiar",
        "Moderately familiar",
        "Very familiar",
        "Extremely familiar",
    ],
    "preferred_output": ["Clean dataset", "Figures", "Slides", "Full report", "Other"],
    "confidence_running_pipeline": [
        "Not confident",
        "Slightly confident",
        "Moderately confident",
        "Very confident",
        "Extremely confident",
    ],
}

DISPLAY_NAMES = {
    "role": "Role",
    "workflow_familiarity": "Workflow familiarity",
    "preferred_output": "Preferred output",
    "confidence_running_pipeline": "Pipeline confidence",
}


def normalize_column(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def find_newest_csv(project_root: Path) -> Path:
    raw_root = project_root / "data" / SURVEY_KEY / "raw"
    candidates = sorted(raw_root.rglob("*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        raise SystemExit(
            "No CSV export found. Pass --input tests/fixtures/repo_smoke_test_responses.csv "
            "for the local smoke test, or run export-responses first."
        )
    return candidates[0]


def read_responses(input_csv: Path) -> pd.DataFrame:
    data = pd.read_csv(input_csv)
    data = data.rename(columns={column: normalize_column(str(column)) for column in data.columns})
    data = data.dropna(how="all")
    return data


def write_summary(data: pd.DataFrame, md_path: Path, tex_path: Path) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| Variable | Nonmissing | Unique values |",
        "| --- | ---: | ---: |",
    ]
    tex_rows = [
        r"\begin{tabular}{lrr}",
        r"\hline",
        r"Variable & Nonmissing & Unique values \\",
        r"\hline",
    ]
    for variable, display_name in DISPLAY_NAMES.items():
        if variable not in data.columns:
            lines.append(f"| {display_name} | missing | missing |")
            tex_rows.append(f"{display_name} & missing & missing \\\\")
            continue
        series = data[variable].dropna()
        lines.append(f"| {display_name} | {len(series)} | {series.nunique()} |")
        tex_rows.append(f"{display_name} & {len(series)} & {series.nunique()} \\\\")
    tex_rows.extend([r"\hline", r"\end{tabular}"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tex_path.write_text("\n".join(tex_rows) + "\n", encoding="utf-8")


def make_bar_chart(data: pd.DataFrame, variable: str, choices: list[str], output_stem: Path) -> list[Path]:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    if variable not in data.columns:
        raise SystemExit(f"Expected variable not found: {variable}")

    counts = data[variable].dropna().astype(str).value_counts()
    values = [int(counts.get(choice, 0)) for choice in choices]

    height = max(4.4, 0.58 * len(choices) + 1.6)
    fig, ax = plt.subplots(figsize=(9.6, height))
    ax.barh(choices, values, color="#2f6f8f")
    ax.invert_yaxis()
    ax.set_xlabel("Responses")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim(0, max(1, max(values)) + 0.8)
    ax.tick_params(axis="both", labelsize=11)
    ax.xaxis.label.set_size(11)
    for index, value in enumerate(values):
        ax.text(value + 0.08, index, str(value), va="center", fontsize=11)
    fig.tight_layout()
    pdf_path = output_stem.with_suffix(".pdf")
    png_path = output_stem.with_suffix(".png")
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    return [pdf_path, png_path]


def run_analysis(input_csv: Path | None = None, project_root: Path = PROJECT_ROOT) -> dict[str, Path]:
    if input_csv is None:
        input_csv = find_newest_csv(project_root)
    input_csv = Path(input_csv)
    if not input_csv.is_absolute():
        input_csv = project_root / input_csv
    if not input_csv.exists():
        raise SystemExit(f"Input CSV not found: {input_csv}")

    data = read_responses(input_csv)
    processed_dir = project_root / "data" / SURVEY_KEY / "processed"
    inputs_dir = project_root / "slides" / SURVEY_KEY / "inputs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    inputs_dir.mkdir(parents=True, exist_ok=True)

    clean_csv = processed_dir / "clean.csv"
    data.to_csv(clean_csv, index=False)
    summary_md = inputs_dir / "summary.md"
    summary_tex = inputs_dir / "summary.tex"
    write_summary(data, summary_md, summary_tex)

    figures: list[Path] = []
    for variable, choices in VARIABLES.items():
        output_stem = inputs_dir / variable
        figures.extend(make_bar_chart(data, variable, choices, output_stem))

    print(f"Input CSV: {input_csv}")
    print(f"Clean data: {clean_csv}")
    print(f"Summary: {summary_md}")
    print(f"Summary TeX: {summary_tex}")
    for figure in figures:
        print(f"Figure: {figure}")

    return {"clean_csv": clean_csv, "summary_md": summary_md, "summary_tex": summary_tex, "inputs_dir": inputs_dir}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze the repository smoke-test survey.")
    parser.add_argument("--input", help="CSV response export. Defaults to newest data/repo_smoke_test/raw/*.csv.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_analysis(Path(args.input) if args.input else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
