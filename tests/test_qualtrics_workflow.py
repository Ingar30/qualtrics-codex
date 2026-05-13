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


def test_load_survey_spec_requires_explicit_file() -> None:
    with pytest.raises(SystemExit):
        qw.load_survey_spec(None)


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


def test_response_values_from_row_maps_choice_labels_to_recodes() -> None:
    spec = {
        "questions": [
            {
                "tag": "satisfaction",
                "type": "mc",
                "text": "Satisfied?",
                "choices": ["No", "Yes"],
            },
            {"tag": "feedback", "type": "text", "text": "Feedback?"},
        ]
    }
    row = {"satisfaction": "Yes", "feedback": "Useful"}

    values = qw.response_values_from_row(
        row,
        spec,
        {"satisfaction": "QID1", "feedback": "QID2"},
        row_number=1,
    )

    assert values["QID1"] == 2
    assert values["QID2"] == "Useful"
    assert values["finished"] == 1
    assert values["progress"] == 100


def test_redact_sensitive_text_hides_qualtrics_ids_links_and_tokens() -> None:
    text = (
        "token secret-token survey SV_abc123 block BL_abc123 flow FL_abc123 "
        "response R_abc123456 https://nhh.eu.qualtrics.com/jfe/form/SV_abc123"
    )

    redacted = qw.redact_sensitive_text(text, token="secret-token")

    assert "secret-token" not in redacted
    assert "SV_abc123" not in redacted
    assert "BL_abc123" not in redacted
    assert "FL_abc123" not in redacted
    assert "R_abc123456" not in redacted
    assert "qualtrics.com" not in redacted
    assert "[QUALTRICS_API_TOKEN]" in redacted
    assert "[QUALTRICS_LINK]" in redacted


def test_write_survey_link_slide_inputs_uses_ignored_inputs_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qw, "PROJECT_ROOT", tmp_path)
    link = "https://example.qualtrics.com/jfe/form/SV_fake"

    tex_path, md_path = qw.write_survey_link_slide_inputs("demo", link)

    assert tex_path == tmp_path / "slides" / "demo" / "inputs" / "survey_link.tex"
    assert md_path == tmp_path / "slides" / "demo" / "inputs" / "survey_link.md"
    tex_text = tex_path.read_text(encoding="utf-8")
    assert tex_text.startswith(f"\\url{{{link}}}\n")
    assert "Activate the survey in Qualtrics before using this respondent-facing link." in tex_text
    md_text = md_path.read_text(encoding="utf-8")
    assert md_text.startswith(f"Reusable test link: [{link}]({link})\n")
    assert "Activate the survey in Qualtrics before using this respondent-facing link." in md_text


def test_parser_includes_live_workflow_commands() -> None:
    parser = qw.build_parser()

    auth_args = parser.parse_args(["check-auth"])
    link_args = parser.parse_args(["get-link", "--survey-key", "demo", "--write-slide-inputs"])
    submit_args = parser.parse_args(
        [
            "submit-synthetic-responses",
            "--survey-key",
            "demo",
            "--input",
            "build/fixtures/demo.csv",
        ]
    )

    assert auth_args.func is qw.command_check_auth
    assert link_args.write_slide_inputs is True
    assert submit_args.func is qw.command_submit_synthetic_responses
