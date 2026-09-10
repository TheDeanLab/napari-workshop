# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy>=2,<2.3", "pandas>=2.2,<3", "tifffile>=2025.1,<2026", "scipy>=1.15,<2", "dask[array]>=2025.1,<2027"]
# [tool.uv]
# exclude-newer = "2026-09-10T23:59:59Z"
# ///
"""Prepare a traceable teaching derivative, one source TIFF at a time."""

import argparse
import importlib.metadata
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import tifffile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from napari_workshop.data import load_tables, reduce_volume  # noqa: E402
from napari_workshop.download import checksum, verified  # noqa: E402


def build_dataset(source_folder, output, factor):
    source_manifest = json.loads((ROOT / "data/zenodo-manifest.json").read_text())
    specs = {f["name"]: f for f in source_manifest["files"]}
    metadata = json.loads((ROOT / "data/metadata.json").read_text())
    metadata["preparation_software"] = {
        name: importlib.metadata.version(name) for name in ["numpy", "scipy", "tifffile"]
    }
    metadata.update(
        {
            "spatial_factor": factor,
            "preparation": {
                "method": "Gaussian filter in float32, sigma=(factor-1)/2 source voxels, reflect boundary; sample at 0,factor,...; round/clip uint16",
                "sigma_source_voxels": (factor - 1) / 2,
                "coordinate_transform": "Images scale by spatial_factor; tables remain in original source voxels; origin unchanged.",
                "table_filtering": "None; full original detections and tracks retained.",
                "source_checksums_verified": True,
            },
        }
    )
    output.mkdir(parents=True)
    for c in (0, 1):
        dest = output / f"ch{c}"
        dest.mkdir()
        for t in metadata["timepoints"]:
            name = f"1_CH{c:02d}_{t:06d}.tif"
            candidates = [source_folder / name, source_folder / f"crop_CH{c:02d}" / name]
            source = next((p for p in candidates if p.is_file()), candidates[0])
            if not verified(source, specs[name]):
                raise ValueError(f"Source does not match the published Zenodo file: {name}")
            array = tifffile.imread(source)
            if list(array.shape) != metadata["source_shape_zyx"] or str(array.dtype) != "uint16":
                raise ValueError(f"Unexpected source shape/dtype: {name}")
            reduced = reduce_volume(array, factor)
            tifffile.imwrite(
                dest / f"frame_{t:06d}.tif",
                reduced,
                metadata={"axes": "ZYX"},
                compression="zlib",
                photometric="minisblack",
            )
            print(f"Prepared channel {c}, timepoint {t + 1}/30", flush=True)
    for name in ("detections.csv", "tracks.csv"):
        source = source_folder / name
        if not source.exists():
            source = source_folder / "crop_analysis" / name
        if not verified(source, specs[name]):
            raise ValueError(f"Table differs from Zenodo: {name}")
        shutil.copyfile(source, output / name)
    points, tracks = load_tables(output, metadata)
    metadata["counts"] = {
        "detections": len(points),
        "track_rows": len(tracks),
        "track_ids": len(set(tracks[:, 0])),
    }
    metadata["files"] = [
        {
            "name": str(p.relative_to(output)).replace("\\", "/"),
            "size": p.stat().st_size,
            "checksum": "sha256:" + checksum(p, "sha256"),
        }
        for p in sorted(output.rglob("*"))
        if p.is_file()
    ]
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "data/teaching")
    parser.add_argument("--archive", type=Path, default=ROOT / "dist/teaching.zip")
    parser.add_argument("--factor", type=int, choices=[2, 4, 8], default=4)
    args = parser.parse_args()
    if args.output.exists() or args.archive.exists():
        parser.error(
            "Output dataset or archive already exists. Choose new paths to preserve prior data."
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.archive.parent.mkdir(parents=True, exist_ok=True)
    with (
        tempfile.TemporaryDirectory(dir=args.output.parent, prefix="prepare-") as data_temp,
        tempfile.TemporaryDirectory(dir=args.archive.parent, prefix="archive-") as zip_temp,
    ):
        working = Path(data_temp) / "teaching"
        build_dataset(args.source, working, args.factor)
        archive = Path(zip_temp) / "teaching.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for path in sorted(working.rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(working))
        spec = {
            "name": "teaching.zip",
            "size": archive.stat().st_size,
            "checksum": "sha256:" + checksum(archive, "sha256"),
        }
        working.rename(args.output)
        archive.rename(args.archive)
    manifest = {
        "source_doi": "10.5281/zenodo.22694247",
        "spatial_factor": args.factor,
        "archive": spec,
    }
    # Preparation creates a candidate; published URLs and checksums are updated
    # explicitly only after uploading and verifying the exact archive.
    manifest_path = args.archive.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Created {args.archive}: {spec['size'] / 1e6:.1f} MB")
    print(f"Candidate manifest: {manifest_path}. The published course manifest is unchanged.")


if __name__ == "__main__":
    main()
