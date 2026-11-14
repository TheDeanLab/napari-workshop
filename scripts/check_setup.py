# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["napari[pyqt6]==0.6.6", "numpy>=2,<2.3", "psutil>=7,<8", "imageio>=2.37,<3", "imageio-ffmpeg==0.6.0"]
# [tool.uv]
# exclude-newer = "2026-09-10T23:59:59Z"
# ///
"""Check this Python environment; --gui and --movie add actual graphics/export checks."""

import argparse
import importlib.metadata
import platform
import sys
import tempfile
from pathlib import Path

import numpy as np
import psutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gui", action="store_true")
    parser.add_argument("--movie", action="store_true")
    args = parser.parse_args()
    print(f"Python: {sys.executable}\nPlatform: {platform.platform()} ({platform.machine()})")
    print(
        f"RAM: {psutil.virtual_memory().total / 2**30:.1f} GiB total; {psutil.virtual_memory().available / 2**30:.1f} GiB available"
    )
    for name in ["napari", "numpy", "PyQt6", "imageio-ffmpeg"]:
        print(name, importlib.metadata.version(name))
    if args.movie:
        import imageio.v2 as imageio

        with tempfile.TemporaryDirectory() as temp:
            movie = Path(temp) / "check.mp4"
            with imageio.get_writer(
                movie, fps=5, codec="libx264", pixelformat="yuv420p"
            ) as writer:
                for value in (0, 100, 200):
                    writer.append_data(np.full((64, 64, 3), value, dtype=np.uint8))
            with imageio.get_reader(movie) as reader:
                if reader.count_frames() != 3:
                    raise RuntimeError("Movie encoding check failed")
        print("Movie encoder: wrote and read 3 frames successfully")
    if args.gui:
        import napari
        from vispy import sys_info

        print(sys_info())
        viewer = napari.Viewer(ndisplay=3)
        z, y, x = np.indices((32, 32, 32))
        viewer.add_image(
            ((z - 16) ** 2 + (y - 16) ** 2 + (x - 16) ** 2 < 100).astype(np.uint8),
            name="Practice sphere",
            contrast_limits=(0, 1),
        )
        print("A sphere should appear. Rotate it, then close napari to finish.")
        napari.run()
    print("Checks complete for the Python executable printed above.")
    print(
        "To check the notebook environment, run this with 'uv run python scripts/check_setup.py --movie' or use 00_check_setup.ipynb."
    )


if __name__ == "__main__":
    main()
