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


def test_index_uses_generated_synthetic_responses(tmp_path: Path) -> None:
    build_site.build_index(tmp_path, ["slides.pdf"])

    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "generate_synthetic_responses.py" in index
    assert "build/fixtures/repo_smoke_test_responses.csv" in index
    assert "prompts/start-with-codex.md" in index
    assert "docs/codex-prompt-alternatives.md" in index
    assert "docs/intended-codex-loop.md" in index
    assert "docs/setup-troubleshooting.md" in index
    assert "Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics" in index
    assert "generate the synthetic responses locally" in index
    assert "prompts/discrimination-beliefs-example.md" in index


def test_walkthrough_mentions_qualtrics_metadata_and_link_privacy(tmp_path: Path) -> None:
    build_site.build_walkthrough(tmp_path)

    walkthrough = (tmp_path / "walkthrough.html").read_text(encoding="utf-8")
    assert "ResponseId" in walkthrough
    assert "R_" in walkthrough
    assert "Reusable links" in walkthrough
    assert "Draft or inactive surveys" in walkthrough
