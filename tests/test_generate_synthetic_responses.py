from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import generate_synthetic_responses as gen


def test_generate_synthetic_responses_writes_expected_columns(tmp_path: Path) -> None:
    spec_file = tmp_path / "code" / "demo" / "survey_spec.json"
    spec_file.parent.mkdir(parents=True)
    spec_file.write_text(
        json.dumps(
            {
                "questions": [
                    {"tag": "role", "type": "mc", "text": "Role?", "choices": ["Student", "Researcher"]},
                    {"tag": "feedback", "type": "text", "text": "Feedback?"},
                    {"tag": "intro", "type": "descriptive", "text": "Intro"},
                ]
            }
        ),
        encoding="utf-8",
    )

    output = gen.generate_synthetic_responses(
        "demo",
        spec_file=spec_file,
        output_path=tmp_path / "tests" / "fixtures" / "demo_responses.csv",
        n=4,
        seed=7,
        project_root=tmp_path,
    )

    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    assert output.exists()
    assert rows
    assert list(rows[0].keys()) == ["role", "feedback"]
    assert {row["role"] for row in rows} <= {"Student", "Researcher"}
    assert all(row["feedback"] for row in rows)


def test_response_rows_rejects_nonpositive_n() -> None:
    spec = {"questions": [{"tag": "role", "type": "mc", "text": "Role?", "choices": ["A"]}]}

    with pytest.raises(SystemExit):
        gen.response_rows(spec, n=0, seed=1)


def test_default_paths_use_survey_key(tmp_path: Path) -> None:
    assert gen.default_spec_path("demo", project_root=tmp_path) == tmp_path / "code" / "demo" / "survey_spec.json"
    assert gen.default_output_path("demo", project_root=tmp_path) == tmp_path / "build" / "fixtures" / "demo_responses.csv"
