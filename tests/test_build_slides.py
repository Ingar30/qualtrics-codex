from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import build_slides


def test_auto_build_falls_back_to_python_when_beamer_deck_is_missing(tmp_path: Path) -> None:
    slide_dir = tmp_path / "slides" / "demo"
    slide_dir.mkdir(parents=True)
    (slide_dir / "slides.md").write_text(
        """---
title: Demo
---

# Demo
""",
        encoding="utf-8",
    )

    result = build_slides.build_deck("demo", project_root=tmp_path, python_pdf=False)

    assert result.backend == "python"
    assert result.status == "success"
    assert result.path == tmp_path / "build" / "slides" / "demo" / "slides.html"
    assert "Beamer deck not found" in result.message
    assert result.path.exists()


def test_find_latex_engine_accepts_explicit_executable_path(tmp_path: Path) -> None:
    fake_engine = tmp_path / "latexmk"
    fake_engine.write_text("", encoding="utf-8")

    assert build_slides.find_latex_engine(str(fake_engine)) == str(fake_engine)


def test_latexmk_command_uses_xelatex_pdf_mode(tmp_path: Path) -> None:
    tex_file = tmp_path / "main.tex"
    output_dir = tmp_path / "out"

    command = build_slides.latex_commands("latexmk", tex_file, output_dir)[0]

    assert "-pdfxe" in command
    assert f"-outdir={output_dir}" in command
    assert "main.tex" in command
