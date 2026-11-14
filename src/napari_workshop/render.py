"""Compose workshop scenes and export views without changing their framing.

``create_scene`` owns viewer construction; callers close the returned viewer.
``export_time_series`` writes and verifies movies; ``fit_frame`` only transforms
already captured pixels. Data validation belongs to :mod:`napari_workshop.data`.
"""

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import dask
import imageio.v2 as imageio
import napari
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageOps
from qtpy.QtWidgets import QApplication

from .data import load_images, load_tables


def fit_frame(frame: NDArray[np.uint8], size: tuple[int, int] = (480, 640)) -> NDArray[np.uint8]:
    """Fit captured RGB(A) pixels into a black RGB canvas without cropping.

    Parameters
    ----------
    frame : ndarray of uint8, shape (height, width, 3 or 4)
        Native screenshot pixels. Alpha is discarded; the input is not modified.
    size : tuple of int
        Output (height, width) in pixels. The entire input is resized uniformly
        with Lanczos interpolation and centered; unused space stays black.

    Returns
    -------
    fitted : ndarray of uint8, shape (size[0], size[1], 3)
        New RGB pixels suitable for a PNG or video frame.

    Raises
    ------
    ValueError
        If the input is not uint8 RGB(A), or output dimensions are nonpositive.
    """
    if frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] not in (3, 4):
        raise ValueError("Expected a uint8 RGB or RGBA screenshot")
    height, width = size
    if height <= 0 or width <= 0:
        raise ValueError("Output height and width must be positive")
    rgb = Image.fromarray(frame[:, :, :3])
    fitted = ImageOps.pad(rgb, (width, height), method=Image.Resampling.LANCZOS, color="black")
    return np.array(fitted)


def create_scene(
    folder: str | Path, downsample: int | None = None, lazy: bool = True
) -> tuple[napari.Viewer, dict[str, Any]]:
    """Open a 3D workshop scene with a synchronized acquired-frame annotation.

    This is the shared scene constructor for the standalone renderer and optional
    lessons. The main lesson shows the individual layer calls explicitly.

    Parameters
    ----------
    folder : str or Path
        Dataset directory accepted by ``load_images`` and ``load_tables``.
    downsample : int or None
        Total spatial factor relative to the source grid; None uses the stored
        factor. Image and table transforms retain their shared coordinates.
    lazy : bool
        If True, decode image volumes on demand using a single Dask worker.

    Returns
    -------
    viewer : napari.Viewer
        Open viewer with two image layers, particles, tracks, and frame text.
        The caller owns the viewer and must close it when finished.
    metadata : dict
        Dataset metadata returned by the image loader.

    Raises
    ------
    FileNotFoundError
        If a required image or table is absent.
    ValueError
        If the loaders reject the images, coordinates, or reduction factor.

    See Also
    --------
    napari_workshop.data.load_images : Validate and load the image series.
    export_time_series : Export and verify acquired frames from an open viewer.

    Notes
    -----
    Requires a working Qt/OpenGL desktop. Sets the process-wide Dask scheduler
    to single-threaded. Changing the frame slider updates the text annotation;
    time remains a zero-based acquisition frame, not elapsed seconds.

    Examples
    --------
    >>> viewer, metadata = create_scene("data/teaching")
    >>> viewer.dims.set_current_step(0, 10)
    >>> viewer.close()
    """
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

    def update_frame_label(event=None):
        viewer.text_overlay.text = (
            f"Frame {viewer.dims.current_step[0]} | coordinates in source voxels"
        )

    viewer.dims.events.current_step.connect(update_frame_label)
    update_frame_label()
    viewer.layers["Particles"].visible = False
    viewer.camera.angles = (15, 20, 100)
    viewer.reset_view()
    QApplication.processEvents()
    return viewer, meta


def export_time_series(
    viewer: napari.Viewer,
    output: str | Path,
    timepoints: Sequence[int],
    fps: float = 10,
) -> Path:
    """Export acquired frames to a verified 640 x 480 H.264 movie.

    Capture the viewer's native canvas and fit each entire view into the output
    dimensions. Aspect ratio is preserved with black padding, including on
    high-DPI displays. The viewer must already contain the intended scene.

    Parameters
    ----------
    viewer : napari.Viewer
        Open 2D or 3D scene whose first dimension is acquisition frame.
    output : str or Path
        New directory for the movie, first/last PNGs, and ``export.json``.
        Existing directories are rejected to preserve prior outputs.
    timepoints : sequence of int
        Nonempty sequence of valid zero-based frame indices to render in order.
    fps : float
        Positive playback frames per second, not the acquisition rate.

    Returns
    -------
    movie : Path
        Verified ``time-series.mp4`` inside the new output directory.

    Raises
    ------
    FileExistsError
        If the output directory already exists.
    ValueError
        If no frames are requested or playback fps is nonpositive.
    RuntimeError
        If the decoded movie has an unexpected frame count or dimensions.

    See Also
    --------
    create_scene : Construct the workshop's standard 3D scene.
    fit_frame : Fit native screenshot pixels without changing their framing.

    Notes
    -----
    Requires a working Qt/OpenGL viewer and FFmpeg encoder. Leaves the viewer
    at the final frame and updates its text overlay with frame/playback labels.
    Does not close the viewer or alter camera framing. Partial outputs remain
    available for diagnosis if encoding fails; retry in a new directory.

    Examples
    --------
    >>> viewer, metadata = create_scene("data/teaching")
    >>> movie = export_time_series(viewer, "outputs/new-run", metadata["timepoints"])
    >>> viewer.close()
    """
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
            frame = fit_frame(viewer.screenshot(canvas_only=True))
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
