from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import render_slides


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LATEX_ENGINE_CANDIDATES = ["latexmk", "xelatex", "pdflatex", "lualatex", "tectonic"]


@dataclass
class BuildResult:
    backend: str
    status: str
    path: Path | None
    message: str


def resolve_executable(command: str) -> str | None:
    candidate = Path(command)
    if candidate.is_absolute() and candidate.exists():
        return str(candidate)
    return shutil.which(command)


def find_latex_engine(requested: str | None = None) -> str | None:
    if requested:
        return resolve_executable(requested)
    for command in LATEX_ENGINE_CANDIDATES:
        resolved = resolve_executable(command)
        if resolved:
            return resolved
    return None


def engine_kind(executable: str) -> str:
    name = Path(executable).name.lower()
    for suffix in (".exe", ".cmd", ".bat"):
        if name.endswith(suffix):
            name = name.removesuffix(suffix)
    return name


def latex_commands(engine: str, tex_file: Path, output_dir: Path) -> list[list[str]]:
    kind = engine_kind(engine)
    if kind == "latexmk":
        return [
            [
                engine,
                "-pdfxe",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                f"-outdir={output_dir}",
                tex_file.name,
            ]
        ]
    if kind == "tectonic":
        return [[engine, "--outdir", str(output_dir), tex_file.name]]
    command = [
        engine,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={output_dir}",
        tex_file.name,
    ]
    return [command, command]


def summarize_failure(result: subprocess.CompletedProcess[str]) -> str:
    output = "\n".join(part for part in [result.stdout, result.stderr] if part)
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        return f"LaTeX exited with code {result.returncode}."
    tail = "\n".join(lines[-18:])
    return f"LaTeX exited with code {result.returncode}. Last log lines:\n{tail}"


def compile_beamer(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    latex_engine: str | None = None,
) -> BuildResult:
    survey_key = render_slides.safe_survey_key(survey_key)
    source_dir = project_root / "slides" / survey_key
    tex_file = source_dir / "main.tex"
    if not tex_file.exists():
        return BuildResult("beamer", "skipped", None, f"Beamer deck not found: {tex_file}")

    engine = find_latex_engine(latex_engine)
    if not engine:
        requested = f" requested engine {latex_engine!r}" if latex_engine else " latexmk/xelatex/pdflatex/lualatex/tectonic"
        return BuildResult("beamer", "skipped", None, f"Could not locate{requested}.")

    output_dir = project_root / "build" / "slides" / survey_key / "beamer"
    output_dir.mkdir(parents=True, exist_ok=True)

    for command in latex_commands(engine, tex_file, output_dir):
        result = subprocess.run(command, cwd=source_dir, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return BuildResult("beamer", "failed", None, summarize_failure(result))

    compiled_pdf = output_dir / f"{tex_file.stem}.pdf"
    if not compiled_pdf.exists():
        return BuildResult("beamer", "failed", None, f"LaTeX completed, but expected PDF was not created: {compiled_pdf}")

    final_pdf = project_root / "build" / "slides" / survey_key / "slides.pdf"
    final_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(compiled_pdf, final_pdf)
    return BuildResult("beamer", "success", final_pdf, f"Built Beamer PDF with {engine_kind(engine)}.")


def render_python_fallback(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    browser: str | None = None,
    try_pdf: bool = True,
) -> BuildResult:
    html_file = render_slides.render_slides(survey_key, project_root=project_root)
    if not try_pdf:
        return BuildResult("python", "success", html_file, "Rendered native Python HTML slides.")

    browser_path = browser or render_slides.find_browser()
    if not browser_path:
        return BuildResult("python", "success", html_file, "Rendered native Python HTML slides. Browser PDF export was skipped.")

    try:
        pdf_file = render_slides.export_pdf(html_file, html_file.with_suffix(".pdf"), browser=browser_path)
    except SystemExit as exc:
        return BuildResult("python", "success", html_file, f"Rendered native Python HTML slides. Browser PDF export failed: {exc}")
    return BuildResult("python", "success", pdf_file, "Rendered native Python HTML slides and PDF.")


def build_deck(
    survey_key: str,
    project_root: Path = PROJECT_ROOT,
    mode: str = "auto",
    latex_engine: str | None = None,
    browser: str | None = None,
    python_pdf: bool = True,
) -> BuildResult:
    if mode == "python":
        return render_python_fallback(survey_key, project_root=project_root, browser=browser, try_pdf=python_pdf)

    beamer = compile_beamer(survey_key, project_root=project_root, latex_engine=latex_engine)
    if beamer.status == "success" or mode == "beamer":
        return beamer

    fallback = render_python_fallback(survey_key, project_root=project_root, browser=browser, try_pdf=python_pdf)
    fallback.message = f"{beamer.message}\nFell back to native Python slides. {fallback.message}"
    return fallback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build slides with Beamer first, then native Python fallback.")
    parser.add_argument("--survey-key", default="repo_smoke_test")
    parser.add_argument("--mode", choices=["auto", "beamer", "python"], default="auto")
    parser.add_argument("--latex-engine", help="Specific LaTeX command or executable path to use for Beamer.")
    parser.add_argument("--browser", help="Path to Chrome, Edge, or Chromium for Python fallback PDF export.")
    parser.add_argument("--no-python-pdf", action="store_true", help="Do not attempt browser PDF export on Python fallback.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = build_deck(
        args.survey_key,
        mode=args.mode,
        latex_engine=args.latex_engine,
        browser=args.browser,
        python_pdf=not args.no_python_pdf,
    )
    print(result.message)
    if result.path:
        print(f"Slide output: {result.path}")
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
