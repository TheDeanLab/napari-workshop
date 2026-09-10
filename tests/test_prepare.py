"""A failed preparation must not publish a partial dataset or archive."""

import importlib.util
import json
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


def test_preparation_preserves_published_manifest(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "prepare_teaching", root / "scripts/prepare_teaching_data.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    published = tmp_path / "data/teaching-manifest.json"
    published.parent.mkdir()
    original = '{"doi": "published-record", "archive": {"checksum": "published-hash"}}\n'
    published.write_text(original)

    def tiny_dataset(source, output, factor):
        output.mkdir()
        (output / "metadata.json").write_text("{}")

    monkeypatch.setattr(module, "build_dataset", tiny_dataset)
    monkeypatch.setattr(sys, "argv", ["prepare_teaching_data.py", "--source", str(tmp_path)])
    module.main()
    assert published.read_text() == original
    candidate = json.loads((tmp_path / "dist/teaching.manifest.json").read_text())
    assert candidate["archive"]["checksum"].startswith("sha256:")
    assert "url" not in candidate["archive"]
    assert (tmp_path / "dist/teaching.zip").is_file()
