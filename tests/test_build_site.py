from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import build_site


def test_page_template_escapes_title() -> None:
    html = build_site.page_template("<demo>", "<main>ok</main>")

    assert "<title>&lt;demo&gt;</title>" in html
    assert "<main>ok</main>" in html


def test_walkthrough_mentions_local_secret_file(tmp_path: Path) -> None:
    build_site.build_walkthrough(tmp_path)

    walkthrough = (tmp_path / "walkthrough.html").read_text(encoding="utf-8")
    assert "qualtrics.env.ps1" in walkthrough
    assert "qualtrics.env" in walkthrough
    assert "QUALTRICS_API_TOKEN" in walkthrough
    assert "qualtrics.com/support/integrations/api-integration/overview" in walkthrough
    assert "generate_synthetic_responses.py" in walkthrough
    assert "check-auth" in walkthrough
    assert "submit-synthetic-responses" in walkthrough


def test_index_starts_with_codex_preferences(tmp_path: Path) -> None:
    build_site.build_index(tmp_path, ["slides.pdf"])

    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "Open prompts/configure-local-preferences.md and follow it as instructions" in index
    assert "Do not summarize it" in index
    assert "QUALTRICS_API_TOKEN" in index
    assert "If Stata, LaTeX, or Qualtrics secrets are missing" in index
    assert "docs/codex-prompt-alternatives.md" in index
    assert "docs/intended-codex-loop.md" in index
    assert "docs/setup-troubleshooting.md" in index
    assert "prompts/configure-local-preferences.md" in index
    assert "SPSS/SAV exports" in index
    assert "CSV exports" in index
    assert "discrimination-beliefs teaching demo" in index
    assert "Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics" in index
    assert "prompts/discrimination-beliefs-example.md" in index
    assert "repo_smoke_test" not in index


def test_walkthrough_mentions_qualtrics_metadata_and_link_privacy(tmp_path: Path) -> None:
    build_site.build_walkthrough(tmp_path)

    walkthrough = (tmp_path / "walkthrough.html").read_text(encoding="utf-8")
    assert "ResponseId" in walkthrough
    assert "R_" in walkthrough
    assert "Reusable links" in walkthrough
    assert "Draft or inactive surveys" in walkthrough
    assert "--format csv" in walkthrough
    assert "--format spss" in walkthrough
    assert "SPSS/SAV" in walkthrough
