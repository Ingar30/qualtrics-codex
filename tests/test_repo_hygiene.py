from __future__ import annotations

import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_private_metadata_directory_is_ignored_for_common_file_types() -> None:
    paths = [
        "data/demo/metadata/survey_info.json",
        "data/demo/metadata/audit.log",
        "data/demo/metadata/notes.txt",
        "data/demo/metadata/responses.csv",
    ]

    result = subprocess.run(
        ["git", "check-ignore", *paths],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    ignored = set(result.stdout.splitlines())
    assert ignored == set(paths)
