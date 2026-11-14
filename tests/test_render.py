"""Catch cropped exports, changed aspect ratios, and stale frame annotations."""

import os

import imageio.v2 as imageio
import numpy as np
import pytest

from napari_workshop import render


def test_fit_frame_preserves_wide_canvas_edges_and_adds_black_padding():
    frame = np.full((240, 640, 4), 255, dtype=np.uint8)
    frame[:8, :, :3] = [255, 0, 0]
    frame[-8:, :, :3] = [0, 255, 0]
    result = render.fit_frame(frame)
    assert result.shape == (480, 640, 3)
    np.testing.assert_array_equal(result[120, 0], [255, 0, 0])
    np.testing.assert_array_equal(result[359, 639], [0, 255, 0])
    assert not result[:120].any()
    assert not result[360:].any()
    assert frame.shape == (240, 640, 4)


def test_fit_frame_preserves_tall_canvas_without_stretching():
    frame = np.full((640, 240, 3), 255, dtype=np.uint8)
    frame[:12] = [255, 0, 0]
    frame[-12:] = [0, 255, 0]
    result = render.fit_frame(frame)
    assert result.shape == (480, 640, 3)
    np.testing.assert_array_equal(result[0, 230], [255, 0, 0])
    np.testing.assert_array_equal(result[-1, 409], [0, 255, 0])
    assert not result[:, :230].any()
    assert not result[:, 410:].any()


@pytest.mark.gui
@pytest.mark.skipif(not os.environ.get("NAPARI_WORKSHOP_GUI_TESTS"), reason="requires a desktop")
def test_scene_annotation_follows_frame_after_export(dataset, tmp_path):
    viewer, _ = render.create_scene(dataset, lazy=False)
    try:
        viewer.dims.set_current_step(0, 1)
        assert viewer.text_overlay.text.startswith("Frame 1 |")
        render.export_time_series(viewer, tmp_path / "movie", [0, 1], fps=5)
        viewer.dims.set_current_step(0, 0)
        assert viewer.text_overlay.text.startswith("Frame 0 |")
    finally:
        viewer.close()


@pytest.mark.gui
@pytest.mark.skipif(not os.environ.get("NAPARI_WORKSHOP_GUI_TESTS"), reason="requires a desktop")
def test_movie_keeps_edge_features_of_native_view(tmp_path):
    import napari
    from qtpy.QtWidgets import QApplication

    image = np.zeros((2, 400, 800), dtype=np.uint8)
    image[:, 30:90, 30:90] = 255
    image[:, 310:370, 710:770] = 255
    viewer = napari.Viewer()
    try:
        viewer.window.resize(1100, 750)
        viewer.add_image(image, contrast_limits=(0, 255))
        QApplication.processEvents()
        viewer.reset_view()
        QApplication.processEvents()
        original_zoom = viewer.camera.zoom
        original_center = viewer.camera.center
        path = render.export_time_series(viewer, tmp_path / "movie", [0, 1], fps=5)
        with imageio.get_reader(path) as reader:
            frame = reader.get_data(0)
            assert reader.count_frames() == 2
        # Both bright edge objects must survive, even on a high-DPI display.
        assert (frame[:240, :160].mean(axis=2) > 200).sum() > 50
        assert (frame[240:, 480:].mean(axis=2) > 200).sum() > 50
        assert viewer.camera.zoom == original_zoom
        assert viewer.camera.center == original_center
    finally:
        viewer.close()


@pytest.mark.gui
@pytest.mark.skipif(not os.environ.get("NAPARI_WORKSHOP_GUI_TESTS"), reason="requires a desktop")
def test_projection_fallback_survives_both_scene_transitions(dataset):
    from pathlib import Path

    import napari
    import nbformat

    from napari_workshop.data import load_images, load_tables

    images, image_scale, metadata = load_images(dataset, lazy=False)
    detections, tracks = load_tables(dataset, metadata)
    viewer = napari.Viewer()
    try:
        dna = viewer.add_image(images[0])
        mito = viewer.add_image(images[1])
        namespace = dict(
            viewer=viewer,
            dna=dna,
            mito=mito,
            USE_3D=False,
            images=images,
            image_scale=image_scale,
            detections=detections,
            tracks=tracks,
            point_scale=(1, 1, 1, 1),
            spacing=1,
        )
        notebook = nbformat.read(
            Path(__file__).resolve().parents[1] / "notebooks/01_rendering_workshop.ipynb",
            as_version=4,
        )
        exec(notebook.cells[18].source, namespace)
        assert viewer.dims.ndisplay == 2
        viewer.layers.clear()
        projection = viewer.add_image(images[0].max(axis=1), name="DNA projection")
        viewer.add_points(detections[["t", "y", "x"]].to_numpy(), name="Particles")
        viewer.add_tracks(tracks[:, [0, 1, 3, 4]], name="Tracks")
        exec(notebook.cells[30].source, namespace)
        assert viewer.dims.ndisplay == 2
        assert viewer.layers["DNA projection"] is projection
        assert "Particles" in viewer.layers and "Tracks" in viewer.layers
    finally:
        viewer.close()
