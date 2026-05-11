from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import qualtrics_workflow as qw


def test_build_base_url_accepts_datacenter_or_host() -> None:
    assert qw.build_base_url("iad1") == "https://iad1.qualtrics.com/API/v3"
    assert qw.build_base_url("https://iad1.qualtrics.com/API/v3") == "https://iad1.qualtrics.com/API/v3"


def test_safe_survey_key_rejects_paths() -> None:
    assert qw.safe_survey_key("my_survey") == "my_survey"
    with pytest.raises(SystemExit):
        qw.safe_survey_key("../secret")
    with pytest.raises(SystemExit):
        qw.safe_survey_key("bad/name")


def test_load_survey_spec_validates_tags(tmp_path: Path) -> None:
    spec = tmp_path / "survey_spec.json"
    spec.write_text(
        json.dumps(
            {
                "questions": [
                    {
                        "tag": "belief",
                        "type": "mc",
                        "text": "What do you think?",
                        "choices": ["A", "B"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    loaded = qw.load_survey_spec(str(spec))
    assert loaded["questions"][0]["tag"] == "belief"


def test_export_payload_defaults_to_compressed_csv() -> None:
    payload = qw.export_payload("csv")
    assert payload["format"] == "csv"
    assert payload["compress"] is True
    assert payload["useLabels"] is True


def test_safe_extract_blocks_zip_slip(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("../escape.txt", "bad")
    with pytest.raises(SystemExit):
        qw.safe_extract(archive, tmp_path / "out")
