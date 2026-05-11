from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import render_slides


def test_render_slides_writes_html_and_copies_assets(tmp_path: Path) -> None:
    source_dir = tmp_path / "slides" / "demo" / "inputs"
    source_dir.mkdir(parents=True)
    (source_dir / "figure.png").write_bytes(b"not really a png")
    (source_dir / "summary.md").write_text(
        "| Variable | Count |\n| --- | ---: |\n| Role | 3 |\n",
        encoding="utf-8",
    )
    (tmp_path / "slides" / "demo" / "slides.md").write_text(
        """---
title: Demo Deck
subtitle: Native HTML
---

# Demo Deck

---

## Summary

{{ include inputs/summary.md }}

---

## Figure

![Figure caption](inputs/figure.png)
""",
        encoding="utf-8",
    )

    output = render_slides.render_slides("demo", project_root=tmp_path)
    html = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "Demo Deck" in html
    assert "<table>" in html
    assert "inputs/figure.png" in html
    assert (tmp_path / "build" / "slides" / "demo" / "inputs" / "figure.png").exists()
