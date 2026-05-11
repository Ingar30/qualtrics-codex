from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_analysis


def test_auto_analysis_falls_back_to_python_when_stata_script_is_missing(tmp_path: Path) -> None:
    script_dir = tmp_path / "code" / "demo" / "analysis"
    script_dir.mkdir(parents=True)
    marker = tmp_path / "analysis-ran.txt"
    (script_dir / "run.py").write_text(
        "from pathlib import Path\nPath('analysis-ran.txt').write_text('ok', encoding='utf-8')\n",
        encoding="utf-8",
    )

    result = run_analysis.run_analysis("demo", project_root=tmp_path)

    assert result.backend == "python"
    assert result.status == "success"
    assert "Stata analysis script not found" in result.message
    assert marker.exists()


def test_find_stata_executable_returns_none_for_missing_explicit_path() -> None:
    assert run_analysis.find_stata_executable("__definitely_missing_stata__") is None


def test_resolve_input_csv_prefers_explicit_relative_path(tmp_path: Path) -> None:
    explicit = Path("tests/fixture.csv")

    assert run_analysis.resolve_input_csv(tmp_path, "demo", explicit) == tmp_path / explicit


def test_stata_do_file_prefers_lab_style_pipeline(tmp_path: Path) -> None:
    pipeline = tmp_path / "scripts" / "stata" / "survey_pipeline.do"
    cleaning = tmp_path / "code" / "demo" / "cleaning" / "run.do"
    figures = tmp_path / "code" / "demo" / "figures" / "run.do"
    for path in [pipeline, cleaning, figures]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("* test\n", encoding="utf-8")

    do_file, label = run_analysis.stata_do_file(tmp_path, "demo")

    assert do_file == pipeline
    assert label == "Stata cleaning/figures pipeline"


def test_stata_setup_guidance_mentions_windows_env_var(monkeypatch) -> None:
    monkeypatch.setattr(run_analysis.platform, "system", lambda: "Windows")

    message = run_analysis.stata_setup_guidance()

    assert "STATA_EXE" in message
    assert "Stata19" in message
    assert "qualtrics.env.ps1" in message
