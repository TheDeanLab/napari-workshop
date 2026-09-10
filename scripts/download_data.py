# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = []
# ///
"""Download the small teaching package or selected source timepoints."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from napari_workshop.download import download_file, extract_teaching  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["teaching", "source"], default="teaching")
    parser.add_argument("--timepoints", type=int, default=5, help="First N source frames, 1–30")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--local-source", type=Path, help="Reuse checksum-matching local source files"
    )
    args = parser.parse_args()
    if not 1 <= args.timepoints <= 30:
        parser.error("--timepoints must be between 1 and 30")
    if args.dataset == "teaching":
        manifest = json.loads((ROOT / "data/teaching-manifest.json").read_text())
        specs = [manifest["archive"]]
        destination = ROOT / "data/downloads"
    else:
        manifest = json.loads((ROOT / "data/zenodo-manifest.json").read_text())
        names = {f"1_CH{c:02d}_{t:06d}.tif" for c in (0, 1) for t in range(args.timepoints)}
        names.update(["detections.csv", "tracks.csv"])
        specs = [s for s in manifest["files"] if s["name"] in names]
        if len(specs) != len(names):
            raise ValueError("Published manifest lacks requested files")
        destination = ROOT / "data/source"
    total = sum(f["size"] for f in specs)
    print(f"{len(specs)} files, {total / 1e6:.1f} MB; destination: {destination}")
    print("Source DOI: https://doi.org/10.5281/zenodo.22694247")
    if args.dry_run:
        return
    for spec in specs:
        local = None
        if args.local_source is not None:
            candidates = [args.local_source / spec["name"]]
            if spec["name"].endswith(".tif"):
                candidates.append(args.local_source / f"crop_CH{spec['name'][4:6]}" / spec["name"])
            else:
                candidates.append(args.local_source / "crop_analysis" / spec["name"])
            local = next((f for f in candidates if f.is_file()), None)
            if local is None:
                raise FileNotFoundError(f"Cannot find local source for {spec['name']}")
        downloaded = download_file(spec, destination, local_file=local)
    if args.dataset == "teaching":
        extract_teaching(downloaded, ROOT / "data/teaching")
    else:
        meta = json.loads((ROOT / "data/metadata.json").read_text())
        meta["timepoints"] = list(range(args.timepoints))
        (destination / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("Ready. Open notebooks/01_rendering_workshop.ipynb in JupyterLab.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(str(error)) from error
