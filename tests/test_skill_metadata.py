from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / ".agents" / "skills"


def skill_frontmatter(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"{path} is missing opening front matter"
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            return lines[1:index]
    raise AssertionError(f"{path} is missing closing front matter")


def test_skill_frontmatter_descriptions_quote_yaml_sensitive_colons() -> None:
    for path in sorted(SKILL_ROOT.glob("*/SKILL.md")):
        for line in skill_frontmatter(path):
            if not line.startswith("description:"):
                continue
            value = line.split(":", 1)[1].strip()
            is_quoted = value.startswith('"') or value.startswith("'")
            assert is_quoted or ": " not in value, f"{path} has an unquoted YAML-sensitive description"
