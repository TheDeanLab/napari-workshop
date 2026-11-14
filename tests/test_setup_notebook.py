"""Exercise the learner's actual readiness cell on unusable datasets."""

import json
from pathlib import Path

import nbformat
import pytest

from napari_workshop.download import checksum


def run_data_check(folder):
    notebook = nbformat.read(
        Path(__file__).resolve().parents[1] / "notebooks/00_check_setup.ipynb", as_version=4
    )
    cell = next(cell for cell in notebook.cells if cell.id == "c5d125ed")
    exec(cell.source, {"DATA": folder})


@pytest.fixture
def verified_dataset(dataset):
    metadata_path = dataset / "metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["files"] = [
        {
            "name": path.relative_to(dataset).as_posix(),
            "size": path.stat().st_size,
            "checksum": "sha256:" + checksum(path, "sha256"),
        }
        for path in dataset.rglob("*")
        if path.is_file() and path != metadata_path
    ]
    metadata_path.write_text(json.dumps(metadata))
    return dataset


def test_readiness_accepts_complete_dataset(verified_dataset):
    run_data_check(verified_dataset)


@pytest.mark.parametrize("name", ["ch1/frame_000001.tif", "tracks.csv"])
def test_readiness_rejects_missing_required_file(verified_dataset, name):
    (verified_dataset / name).unlink()
    with pytest.raises((FileNotFoundError, ValueError)):
        run_data_check(verified_dataset)


def test_readiness_rejects_empty_tiff(verified_dataset):
    (verified_dataset / "ch0/frame_000000.tif").write_bytes(b"")
    with pytest.raises(ValueError):
        run_data_check(verified_dataset)


def test_readiness_rejects_readable_but_altered_table(verified_dataset):
    with (verified_dataset / "detections.csv").open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError, match="[Cc]hecksum|[Vv]erification|[Cc]orrupt"):
        run_data_check(verified_dataset)
