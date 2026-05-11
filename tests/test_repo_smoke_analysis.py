from __future__ import annotations

import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_analysis_module():
    path = PROJECT_ROOT / "code" / "repo_smoke_test" / "analysis" / "run.py"
    spec = importlib.util.spec_from_file_location("repo_smoke_analysis", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repo_smoke_analysis_writes_outputs(tmp_path: Path) -> None:
    module = load_analysis_module()
    fixture = PROJECT_ROOT / "tests" / "fixtures" / "repo_smoke_test_responses.csv"
    outputs = module.run_analysis(fixture, project_root=tmp_path)

    assert outputs["clean_csv"].exists()
    assert outputs["summary_md"].exists()
    assert outputs["summary_tex"].exists()
    assert (outputs["inputs_dir"] / "role.png").exists()
    assert (outputs["inputs_dir"] / "role.pdf").exists()
    assert (outputs["inputs_dir"] / "workflow_familiarity.png").exists()
    assert (outputs["inputs_dir"] / "workflow_familiarity.pdf").exists()
    assert "Pipeline confidence" in outputs["summary_md"].read_text(encoding="utf-8")


def test_read_responses_drops_qualtrics_metadata_rows(tmp_path: Path) -> None:
    module = load_analysis_module()
    fixture = tmp_path / "qualtrics_export.csv"
    fixture.write_text(
        "\n".join(
            [
                "ResponseId,role,workflow_familiarity,preferred_output,confidence_running_pipeline",
                "Response ID,Which role?,How familiar?,Preferred output?,Confidence?",
                "ImportId,response_import,workflow_import,output_import,confidence_import",
                "R_abc123,Researcher,Very familiar,Slides,Very confident",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    data = module.read_responses(fixture)

    assert len(data) == 1
    assert data.iloc[0]["responseid"] == "R_abc123"
    assert data.iloc[0]["role"] == "Researcher"
