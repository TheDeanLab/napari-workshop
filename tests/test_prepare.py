"""A failed preparation must not publish a partial dataset or archive."""

import subprocess
import sys
from pathlib import Path


def test_missing_source_leaves_final_destinations_absent(tmp_path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "teaching"
    archive = tmp_path / "teaching.zip"
    result = subprocess.run(
        [
            sys.executable,
            str(root / "scripts/prepare_teaching_data.py"),
            "--source",
            str(tmp_path / "missing"),
            "--output",
            str(output),
            "--archive",
            str(archive),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Source does not match" in result.stderr
    assert not output.exists()
    assert not archive.exists()
