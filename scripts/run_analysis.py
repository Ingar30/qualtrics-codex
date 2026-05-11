from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import render_slides


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATA_COMMANDS = [
    "stata-mp",
    "stata-se",
    "stata-be",
    "stata",
    "StataMP-64",
    "StataSE-64",
    "StataBE-64",
]
WINDOWS_STATA_PATHS = [
    r"C:\Program Files\Stata19\StataMP-64.exe",
    r"C:\Program Files\Stata19\StataSE-64.exe",
    r"C:\Program Files\Stata19\StataBE-64.exe",
    r"C:\Program Files\Stata18\StataMP-64.exe",
    r"C:\Program Files\Stata18\StataSE-64.exe",
    r"C:\Program Files\Stata18\StataBE-64.exe",
    r"C:\Program Files\Stata17\StataMP-64.exe",
    r"C:\Program Files\Stata17\StataSE-64.exe",
    r"C:\Program Files\Stata17\StataBE-64.exe",
]


@dataclass
class AnalysisResult:
    backend: str
    status: str
    message: str


def resolve_executable(command: str) -> str | None:
    candidate = Path(command)
    if candidate.is_absolute() and candidate.exists():
        return str(candidate)
    return shutil.which(command)


def find_stata_executable(requested: str | None = None) -> str | None:
    env_value = os.environ.get("STATA_EXE")
    candidates: list[str] = []
    if requested:
        candidates.append(requested)
    if env_value:
        candidates.append(env_value)
    candidates.extend(STATA_COMMANDS)
    if platform.system() == "Windows":
        candidates.extend(WINDOWS_STATA_PATHS)
    for candidate in candidates:
        resolved = resolve_executable(candidate)
        if resolved:
            return resolved
    return None


def stata_setup_guidance() -> str:
    if platform.system() == "Windows":
        return (
            "Could not locate Stata. Set STATA_EXE to your Stata executable, for example: "
            '$env:STATA_EXE = "C:\\Program Files\\Stata19\\StataMP-64.exe". '
            "To persist it, add that line to $HOME\\.secrets\\qualtrics.env.ps1 or your PowerShell profile."
        )
    return "Could not locate Stata. Install Stata on PATH or set STATA_EXE to the Stata executable."


def find_newest_response_file(project_root: Path, survey_key: str) -> Path | None:
    raw_root = project_root / "data" / survey_key / "raw"
    if not raw_root.exists():
        return None
    candidates = sorted(
        [path for path in raw_root.rglob("*") if path.suffix.lower() in {".csv", ".sav"}],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def find_newest_csv(project_root: Path, survey_key: str) -> Path | None:
    raw_root = project_root / "data" / survey_key / "raw"
    if not raw_root.exists():
        return None
    candidates = sorted(raw_root.rglob("*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def resolve_input_file(project_root: Path, survey_key: str, input_file: Path | None) -> Path | None:
    if input_file is None:
        return find_newest_response_file(project_root, survey_key)
    if input_file.is_absolute():
        return input_file
    return project_root / input_file


def resolve_input_csv(project_root: Path, survey_key: str, input_csv: Path | None) -> Path | None:
    return resolve_input_file(project_root, survey_key, input_csv)


def stata_do_file(project_root: Path, survey_key: str) -> tuple[Path | None, str]:
    lab_pipeline = project_root / "scripts" / "stata" / "survey_pipeline.do"
    cleaning_do = project_root / "code" / survey_key / "cleaning" / "run.do"
    figures_do = project_root / "code" / survey_key / "figures" / "run.do"
    if lab_pipeline.exists() and cleaning_do.exists() and figures_do.exists():
        return lab_pipeline, "Stata cleaning/figures pipeline"

    analysis_do = project_root / "code" / survey_key / "analysis" / "run.do"
    if analysis_do.exists():
        return analysis_do, "Stata analysis script"
    return None, "Stata analysis script"


def stata_command(stata_exe: str, do_file: Path, project_root: Path, survey_key: str, input_csv: Path) -> list[str]:
    args = [str(do_file), str(project_root), survey_key, str(input_csv)]
    if platform.system() == "Windows":
        return [stata_exe, "/e", "do", *args]
    return [stata_exe, "-b", "do", *args]


def summarize_subprocess_failure(result: subprocess.CompletedProcess[str], tool: str) -> str:
    output = "\n".join(part for part in [result.stdout, result.stderr] if part)
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        return f"{tool} exited with code {result.returncode}."
    return f"{tool} exited with code {result.returncode}. Last log lines:\n" + "\n".join(lines[-18:])


def run_stata_analysis(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    input_csv: Path | None = None,
    stata_exe: str | None = None,
) -> AnalysisResult:
    survey_key = render_slides.safe_survey_key(survey_key)
    do_file, do_label = stata_do_file(project_root, survey_key)
    if not do_file:
        return AnalysisResult("stata", "skipped", f"Stata analysis script not found for {survey_key}.")

    resolved_input = resolve_input_file(project_root, survey_key, input_csv)
    if not resolved_input or not resolved_input.exists():
        return AnalysisResult("stata", "skipped", "No CSV or SAV input found for Stata analysis.")

    resolved_stata = find_stata_executable(stata_exe)
    if not resolved_stata:
        return AnalysisResult("stata", "skipped", stata_setup_guidance())

    command = stata_command(resolved_stata, do_file, project_root, survey_key, resolved_input)
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return AnalysisResult("stata", "failed", summarize_subprocess_failure(result, "Stata"))
    return AnalysisResult("stata", "success", f"Ran {do_label}.")


def run_python_analysis(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    input_csv: Path | None = None,
) -> AnalysisResult:
    survey_key = render_slides.safe_survey_key(survey_key)
    script = project_root / "code" / survey_key / "analysis" / "run.py"
    if not script.exists():
        return AnalysisResult("python", "failed", f"Python analysis script not found: {script}")
    if input_csv is not None and Path(input_csv).suffix.lower() == ".sav":
        return AnalysisResult("python", "failed", "Python fallback expects CSV input. Use Stata for SAV exports or export CSV.")

    command = [sys.executable, str(script)]
    if input_csv is not None:
        command.extend(["--input", str(input_csv)])
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return AnalysisResult("python", "failed", summarize_subprocess_failure(result, "Python analysis"))
    return AnalysisResult("python", "success", result.stdout.strip() or "Ran Python analysis.")


def run_analysis(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    input_csv: Path | None = None,
    mode: str = "auto",
    stata_exe: str | None = None,
) -> AnalysisResult:
    if mode == "python":
        return run_python_analysis(survey_key, project_root=project_root, input_csv=input_csv)

    stata = run_stata_analysis(survey_key, project_root=project_root, input_csv=input_csv, stata_exe=stata_exe)
    if stata.status == "success" or mode == "stata":
        return stata

    python = run_python_analysis(survey_key, project_root=project_root, input_csv=input_csv)
    if python.status == "success":
        python.message = f"{stata.message}\nFell back to Python analysis.\n{python.message}"
    return python


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run survey analysis with Stata first, then Python fallback.")
    parser.add_argument("--survey-key", default="repo_smoke_test")
    parser.add_argument("--input", help="CSV response export. Defaults to newest data/<survey_key>/raw/*.csv.")
    parser.add_argument("--mode", choices=["auto", "stata", "python"], default="auto")
    parser.add_argument("--stata-exe", help="Path to a Stata executable. Overrides STATA_EXE.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_analysis(
        args.survey_key,
        input_csv=Path(args.input) if args.input else None,
        mode=args.mode,
        stata_exe=args.stata_exe,
    )
    print(result.message)
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
