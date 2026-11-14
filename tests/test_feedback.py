"""Exercise the learner entry points implicated by workshop feedback."""

import os
import runpy
import sys
import textwrap
from pathlib import Path

import imageio.v2 as imageio
import napari
import nbformat
import numpy as np
import pytest
from qtpy.QtWidgets import QApplication

from napari_workshop.render import fit_frame

ROOT = Path(__file__).resolve().parents[1]
GUI = pytest.mark.skipif(
    not os.environ.get("NAPARI_WORKSHOP_GUI_TESTS"), reason="requires a desktop"
)


@pytest.mark.gui
@GUI
@pytest.mark.parametrize("entry", ["script", "notebook"])
def test_setup_sphere_is_visible(entry, monkeypatch):
    try:
        if entry == "script":
            monkeypatch.setattr(sys, "argv", ["check_setup.py", "--gui"])
            monkeypatch.setattr(napari, "run", lambda: None)
            runpy.run_path(str(ROOT / "scripts/check_setup.py"), run_name="__main__")
        else:
            nb = nbformat.read(ROOT / "notebooks/00_check_setup.ipynb", as_version=4)
            source = next(c.source for c in nb.cells if c.id == "2e1b27db")
            exec(source.replace("%gui qt\n", ""), {})
        viewer = napari.current_viewer()
        QApplication.processEvents()
        viewer.reset_view()
        QApplication.processEvents()
        pixels = viewer.screenshot(canvas_only=True)[..., :3]
        assert (pixels.max(axis=2) > 128).sum() > 1000
    finally:
        napari.Viewer.close_all()


@pytest.mark.parametrize(
    "notebook,cell_id,movie",
    [
        ("notebooks/01_rendering_workshop.ipynb", "ebfae9bc", "camera-movie.mp4"),
        ("notebooks/02_optional_animation.ipynb", "a4d77e9b", "rotation.mp4"),
        ("instructor/solutions.ipynb", None, "rotation.mp4"),
    ],
)
def test_camera_export_fits_native_frames(notebook, cell_id, movie, tmp_path, caplog):
    # Isolate encoding from Qt; full notebook execution separately checks real interpolation.
    frame = np.zeros((302, 502, 4), dtype=np.uint8)
    frame[..., 3] = 255
    frame[:, :40, :3] = [255, 0, 0]
    frame[:, -40:, :3] = [0, 255, 0]

    class Animation:
        def animate(self, path, **kwargs):
            path = Path(path)
            if path.suffix:
                with imageio.get_writer(path, fps=10) as writer:
                    writer.append_data(frame)
                    writer.append_data(frame)
            else:
                path.mkdir()
                for index in range(2):
                    imageio.imwrite(path / f"frame_{index:06d}.png", frame)

    nb = nbformat.read(ROOT / notebook, as_version=4)
    cell = next(
        c
        for c in nb.cells
        if c.cell_type == "code"
        and (c.id == cell_id if cell_id else "animation.animate" in c.source)
    )
    # Execute the actual export statements, leaving keyframe creation to the GUI run.
    source = cell.source[cell.source.index("animation.animate") :]
    lines = source.splitlines()
    source = lines[0] + "\n" + textwrap.dedent("\n".join(lines[1:]))
    exec(
        source, dict(animation=Animation(), OUTPUT=tmp_path, imageio=imageio, fit_frame=fit_frame)
    )
    with imageio.get_reader(tmp_path / movie) as reader:
        assert reader.count_frames() == 2
        assert reader.get_meta_data()["fps"] == 10
        decoded = reader.get_data(0)
    assert decoded.shape == (480, 640, 3)
    expected = fit_frame(frame).astype(float)
    assert np.abs(decoded.astype(float) - expected).mean() < 5
    assert "macro_block_size" not in caplog.text
