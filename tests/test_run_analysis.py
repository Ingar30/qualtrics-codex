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
