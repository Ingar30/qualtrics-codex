from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
HELPER = SCRIPTS_DIR / "run_live_validation.py"

sys.path.insert(0, str(SCRIPTS_DIR))

import build_site  # noqa: E402
import run_live_validation  # noqa: E402


BASE_ARGS = [
    "--survey-key",
    "validation_test",
    "--survey-name",
    "Validation Test Survey",
    "--spec-file",
    "code/repo_smoke_test/survey_spec.json",
    "--n",
    "100",
]


def run_helper(*extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HELPER), *BASE_ARGS, *extra],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_dry_run_includes_live_validation_sequence() -> None:
    result = run_helper("--dry-run", "--i-understand-this-calls-qualtrics")

    assert result.returncode == 0, result.stderr
    output = result.stdout
    assert "check-auth" in output
    assert "create-survey" in output
    assert "get-link" in output
    assert "--write-slide-inputs" in output
    assert "generate_synthetic_responses.py" in output
    assert "submit-synthetic-responses" in output
    assert "--limit 1" in output
    assert "--resume" in output
    assert "export-responses" in output
    assert "run_analysis.py" in output
    assert "build_slides.py" in output
    assert "--mode python" in output


def test_helper_refuses_without_live_acknowledgement() -> None:
    result = run_helper("--dry-run")

    assert result.returncode != 0
    assert "--i-understand-this-calls-qualtrics" in result.stderr


def test_command_sequence_contains_expected_guarded_steps() -> None:
    args = argparse.Namespace(
        survey_key="validation_test",
        survey_name="Validation Test Survey",
        spec_file="code/repo_smoke_test/survey_spec.json",
        n=100,
        synthetic_output=None,
        export_format="csv",
        public_host=None,
        dry_run=True,
        i_understand_this_calls_qualtrics=True,
    )

    commands = [run_live_validation.command_text(step.display_argv) for step in run_live_validation.build_steps(args)]
    joined = "\n".join(commands)

    assert any("get-link" in command and "--write-slide-inputs" in command for command in commands)
    assert any("submit-synthetic-responses" in command and "--limit 1" in command for command in commands)
    assert any("submit-synthetic-responses" in command and "--resume" in command for command in commands)
    assert any("run_analysis.py" in command for command in commands)
    assert any("build_slides.py" in command and "--mode auto" in command for command in commands)
    assert any("build_slides.py" in command and "--mode python" in command for command in commands)
    assert joined.count("export-responses") == 2


def test_stata_validation_export_format_uses_spss() -> None:
    args = argparse.Namespace(
        survey_key="validation_test",
        survey_name="Validation Test Survey",
        spec_file="code/repo_smoke_test/survey_spec.json",
        n=100,
        synthetic_output=None,
        export_format="spss",
        public_host=None,
        dry_run=True,
        i_understand_this_calls_qualtrics=True,
    )

    commands = [run_live_validation.command_text(step.display_argv) for step in run_live_validation.build_steps(args)]
    export_commands = [command for command in commands if "export-responses" in command]

    assert export_commands
    assert all("--format spss" in command for command in export_commands)


def test_summary_payload_omits_live_outputs_and_identifiers() -> None:
    args = argparse.Namespace(
        survey_key="validation_test",
        survey_name="Validation Test Survey",
        spec_file="code/repo_smoke_test/survey_spec.json",
        n=100,
        export_format="csv",
        dry_run=False,
    )
    steps = [
        {
            "name": "check-auth",
            "command": "python scripts\\qualtrics_workflow.py check-auth",
            "exit_code": 0,
            "duration_seconds": 0.1,
            "status": "ok",
        }
    ]

    payload = run_live_validation.summary_payload(args, steps, "completed")
    text = json.dumps(payload)

    assert "stdout" not in text
    assert "stderr" not in text
    assert "responseId" not in text
    assert "reusable_link" not in text
    assert "https://" not in text
    assert "QUALTRICS_API_TOKEN" not in text
    assert not re.search(r"\bSV_[A-Za-z0-9]+\b", text)
    assert not re.search(r"\bR_[A-Za-z0-9]+\b", text)


def test_site_validation_page_is_synthetic_only(tmp_path: Path) -> None:
    build_site.build_validation(tmp_path)

    validation = (tmp_path / "validation.html").read_text(encoding="utf-8")
    assert "Validated Full Loop" in validation
    assert "CI and GitHub Pages never call Qualtrics" in validation
    assert "run_live_validation.py" in validation
    assert "synthetic-only" in validation
    assert "https://qualtrics" not in validation.lower()
    assert not re.search(r"\bSV_[A-Za-z0-9]+\b", validation)
    assert not re.search(r"\bR_[A-Za-z0-9]+\b", validation)


def test_site_pages_do_not_publish_live_identifiers(tmp_path: Path) -> None:
    build_site.build_index(tmp_path, ["slides.pdf"])
    build_site.build_walkthrough(tmp_path)
    build_site.build_validation(tmp_path)

    for page in ["index.html", "walkthrough.html", "validation.html"]:
        text = (tmp_path / page).read_text(encoding="utf-8")
        assert "https://qualtrics" not in text.lower()
        assert not re.search(r"\bSV_[A-Za-z0-9]+\b", text)
        assert not re.search(r"\bR_[A-Za-z0-9]+\b", text)


def test_preference_prompt_maps_stata_to_sav_and_python_to_csv() -> None:
    prompt = (PROJECT_ROOT / "prompts" / "configure-local-preferences.md").read_text(encoding="utf-8")
    loop_skill = (PROJECT_ROOT / ".agents" / "skills" / "qualtrics-survey-loop" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    combined = f"{prompt}\n{loop_skill}"

    assert "AGENTS.override.md" in combined
    assert "SPSS/SAV" in combined
    assert "CSV" in combined
    assert "import spss" in combined
    assert "--format spss" in combined
    assert "--format csv" in combined
