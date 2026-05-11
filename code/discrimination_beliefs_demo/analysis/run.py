from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator


SURVEY_KEY = "discrimination_beliefs_demo"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
RESPONSE_ID_COLUMNS = ("responseid", "response_id")


def normalize_column(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")


def display_name(tag: str) -> str:
    return tag.replace("_", " ").title()


def tex_escape(value: str) -> str:
    return value.replace("&", r"\&").replace("_", r"\_")


def load_spec(project_root: Path) -> dict:
    path = project_root / "code" / SURVEY_KEY / "survey_spec.json"
    return json.loads(path.read_text(encoding="utf-8"))


def find_newest_csv(project_root: Path) -> Path:
    raw_root = project_root / "data" / SURVEY_KEY / "raw"
    candidates = sorted(raw_root.rglob("*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        raise SystemExit(
            "No CSV export found. Pass --input build/fixtures/discrimination_beliefs_demo_responses.csv "
            "for the local synthetic demo, or export responses from Qualtrics first."
        )
    return candidates[0]


def read_responses(input_csv: Path) -> pd.DataFrame:
    data = pd.read_csv(input_csv)
    data = data.rename(columns={column: normalize_column(str(column)) for column in data.columns})
    data = data.dropna(how="all")
    for response_id_column in RESPONSE_ID_COLUMNS:
        if response_id_column in data.columns:
            response_ids = data[response_id_column].fillna("").astype(str).str.strip()
            data = data[response_ids.str.startswith("R_")].copy()
            break
    return data


def write_summary(data: pd.DataFrame, questions: list[dict], md_path: Path, tex_path: Path) -> None:
    rows = [question for question in questions if question["type"] == "mc"]
    md_lines = ["| Survey measure | Nonmissing | Unique values |", "| --- | ---: | ---: |"]
    tex_lines = [
        r"\begin{tabular}{lrr}",
        r"\hline",
        r"Survey measure & Nonmissing & Unique values \\",
        r"\hline",
    ]
    for question in rows:
        tag = str(question["tag"])
        label = display_name(tag)
        if tag not in data.columns:
            md_lines.append(f"| {label} | missing | missing |")
            tex_lines.append(f"{tex_escape(label)} & missing & missing \\\\")
            continue
        series = data[tag].dropna()
        md_lines.append(f"| {label} | {len(series)} | {series.nunique()} |")
        tex_lines.append(f"{tex_escape(label)} & {len(series)} & {series.nunique()} \\\\")
    tex_lines.extend([r"\hline", r"\end{tabular}"])
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    tex_path.write_text("\n".join(tex_lines) + "\n", encoding="utf-8")


def make_bar_chart(data: pd.DataFrame, question: dict, output_stem: Path) -> None:
    tag = str(question["tag"])
    choices = [str(choice) for choice in question["choices"]]
    counts = data[tag].dropna().astype(str).value_counts() if tag in data.columns else pd.Series(dtype=int)
    values = [int(counts.get(choice, 0)) for choice in choices]

    fig, ax = plt.subplots(figsize=(10.2, max(4.4, 0.58 * len(choices) + 1.6)))
    ax.barh(choices, values, color="#315f72")
    ax.invert_yaxis()
    ax.set_title(display_name(tag), loc="left", fontsize=14, pad=10)
    ax.set_xlabel("Responses")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim(0, max(1, max(values)) + 1.2)
    for index, value in enumerate(values):
        ax.text(value + 0.12, index, str(value), va="center", fontsize=11)
    fig.tight_layout()
    fig.savefig(output_stem.with_suffix(".pdf"))
    fig.savefig(output_stem.with_suffix(".png"), dpi=220)
    plt.close(fig)


def run_analysis(input_csv: Path | None = None, project_root: Path = PROJECT_ROOT) -> dict[str, Path]:
    input_csv = input_csv or find_newest_csv(project_root)
    if not input_csv.is_absolute():
        input_csv = project_root / input_csv
    if not input_csv.exists():
        raise SystemExit(f"Input CSV not found: {input_csv}")

    spec = load_spec(project_root)
    data = read_responses(input_csv)
    processed_dir = project_root / "data" / SURVEY_KEY / "processed"
    inputs_dir = project_root / "slides" / SURVEY_KEY / "inputs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    inputs_dir.mkdir(parents=True, exist_ok=True)

    clean_csv = processed_dir / "clean.csv"
    data.to_csv(clean_csv, index=False)
    write_summary(data, spec["questions"], inputs_dir / "summary.md", inputs_dir / "summary.tex")
    for question in spec["questions"]:
        if question["type"] == "mc":
            make_bar_chart(data, question, inputs_dir / str(question["tag"]))

    print(f"Input CSV: {input_csv}")
    print(f"Clean data: {clean_csv}")
    print(f"Slide inputs: {inputs_dir}")
    return {"clean_csv": clean_csv, "inputs_dir": inputs_dir}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze the discrimination beliefs demo survey.")
    parser.add_argument("--input", help="CSV response export. Defaults to newest data/discrimination_beliefs_demo/raw/*.csv.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_analysis(Path(args.input) if args.input else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
