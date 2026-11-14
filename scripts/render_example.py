# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["napari[pyqt6]==0.6.6", "numpy>=2,<2.3", "pandas>=2.2,<3", "tifffile>=2025.1,<2026", "scipy>=1.15,<2", "dask[array]>=2025.1,<2027", "imageio>=2.37,<3", "imageio-ffmpeg==0.6.0", "pillow>=11,<13"]
# [tool.uv]
# exclude-newer = "2026-09-10T23:59:59Z"
# ///
"""Render a short real time series, then verify its movie frames."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from napari_workshop.render import create_scene, export_time_series  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data/teaching")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/example")
    parser.add_argument("--downsample", type=int, choices=[1, 2, 4, 8])
    parser.add_argument("--frames", type=int, default=30)
    args = parser.parse_args()
    if args.frames < 1:
        parser.error("--frames must be positive")
    if args.output.exists():
        parser.error("Output folder exists. Choose a new --output folder.")
    viewer, meta = create_scene(args.data, args.downsample)
    try:
        path = export_time_series(viewer, args.output, meta["timepoints"][: args.frames])
        print(f"Movie verified: {path}")
    finally:
        viewer.close()


if __name__ == "__main__":
    main()
