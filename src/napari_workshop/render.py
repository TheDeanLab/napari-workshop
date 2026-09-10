"""Small reproducible rendering helpers; notebook lessons show layer calls directly."""

import json
from pathlib import Path

import dask
import imageio.v2 as imageio
import napari
import numpy as np
from qtpy.QtWidgets import QApplication

from .data import load_images, load_tables


def create_scene(folder, downsample=None, lazy=True):
    """Return a 3D viewer and data metadata for the supplied workshop dataset."""
    # A single local worker bounds simultaneous TIFF decoding.
    dask.config.set(scheduler="single-threaded")
    images, scale, meta = load_images(folder, downsample=downsample, lazy=lazy)
    detections, tracks = load_tables(folder, meta)
    viewer = napari.Viewer(ndisplay=3)
    viewer.window.resize(900, 650)
    for array, name, color, limits in zip(
        images, ["DNA", "Mitochondria"], ["green", "magenta"], [(0, 650), (200, 2400)]
    ):
        viewer.add_image(
            array,
            name=name,
            colormap=color,
            contrast_limits=limits,
            blending="additive",
            scale=scale,
            rendering="mip",
            interpolation3d="linear",
        )
    spacing = meta.get("voxel_size_um") or 1
    point_scale = (1, spacing, spacing, spacing)
    viewer.add_points(
        detections[["t", "z", "y", "x"]].to_numpy(),
        name="Particles",
        size=4 * spacing,
        face_color="cyan",
        border_color="white",
        scale=point_scale,
        opacity=0.7,
    )
    viewer.add_tracks(tracks, name="Tracks", scale=point_scale, tail_length=5, tail_width=2)
    viewer.dims.axis_labels = ("frame", "z", "y", "x")
    viewer.axes.visible = True
    viewer.text_overlay.visible = True
    viewer.text_overlay.text = "Frame 0 | coordinates in source voxels"
    viewer.layers["Particles"].visible = False
    viewer.camera.angles = (15, 20, 100)
    viewer.reset_view()
    QApplication.processEvents()
    return viewer, meta


def export_time_series(viewer, output, timepoints, fps=10):
    """Stream one 640x480 screenshot per acquired frame to H.264 MP4."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    if not timepoints or fps <= 0:
        raise ValueError("At least one timepoint and a positive playback fps are required")
    movie = output / "time-series.mp4"
    with imageio.get_writer(
        movie,
        format="FFMPEG",
        mode="I",
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=16,
    ) as writer:
        for i, t in enumerate(timepoints):
            viewer.dims.set_current_step(0, int(t))
            viewer.text_overlay.text = f"Frame {t} | playback {fps} frames/s"
            QApplication.processEvents()
            frame = viewer.screenshot(canvas_only=True, size=(480, 640))
            if i in (0, len(timepoints) - 1):
                imageio.imwrite(output / f"frame-{t:03d}.png", frame)
            writer.append_data(frame[:, :, :3])
    reader = imageio.get_reader(movie, format="FFMPEG")
    try:
        count = reader.count_frames()
        info = reader.get_meta_data()
        first, last = reader.get_data(0), reader.get_data(count - 1)
    finally:
        reader.close()
    if count != len(timepoints) or first.shape[:2] != (480, 640):
        raise RuntimeError("Exported movie did not match the requested frames/dimensions")
    report = {
        "frame_count": count,
        "fps": info["fps"],
        "size_wh": list(info["size"]),
        "source_timepoints": list(timepoints),
        "camera_angles": list(viewer.camera.angles),
        "camera_center": list(viewer.camera.center),
        "camera_zoom": viewer.camera.zoom,
        "first_last_mean_difference": float(np.abs(first.astype(float) - last).mean()),
    }
    (output / "export.json").write_text(json.dumps(report, indent=2) + "\n")
    return movie
