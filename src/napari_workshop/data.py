"""TIFF time series and tables, kept in a shared source-voxel coordinate system."""

import json
from pathlib import Path

import dask.array as da
import numpy as np
import pandas as pd
import tifffile
from dask import delayed
from scipy.ndimage import gaussian_filter


def reduce_volume(image, factor):
    """Filter then sample the original grid at 0, factor, 2*factor, ... .

    Preserve sampled voxel centers, not the outer image footprint. The last
    source center is omitted unless divisible by factor; coarse display cells
    can extend beyond or stop short of the original edge by < half a coarse cell.
    Tables retain source coordinates; never stretch the reduced grid to fit edges.
    """
    if factor == 1:
        return image
    smooth = gaussian_filter(image.astype(np.float32), sigma=(factor - 1) / 2)
    sampled = smooth[::factor, ::factor, ::factor]
    # Rounding restores uint16 without changing the original files.
    return np.rint(sampled).clip(0, 65535).astype(np.uint16)


def image_path(folder, channel, time):
    """Accept the prepared layout or flat files downloaded from Zenodo."""
    folder = Path(folder)
    prepared = folder / f"ch{channel}" / f"frame_{time:06d}.tif"
    if prepared.is_file():
        return prepared
    source = folder / f"1_CH{channel:02d}_{time:06d}.tif"
    if source.is_file():
        return source
    raise FileNotFoundError(f"Missing channel {channel}, timepoint/frame {time} in {folder}")


def read_volume(path, reduction):
    return reduce_volume(tifffile.imread(path), reduction)


def load_images(folder, downsample=None, lazy=True):
    """Return [channel0, channel1], image scale, metadata. Time stays in frames.

    downsample is the total spatial factor relative to the source grid.
    Lazy arrays contain one delayed task per timepoint and channel. No pixels
    are read here unless lazy=False; callers bound the Dask scheduler to one worker.
    """
    folder = Path(folder)
    meta = json.loads((folder / "metadata.json").read_text())
    base = int(meta["spatial_factor"])
    factor = base if downsample is None else downsample
    if not isinstance(factor, int) or factor not in (1, 2, 4, 8) or factor < base or factor % base:
        raise ValueError(
            f"Downsampling factor must be 1, 2, 4, or 8 and cannot restore resolution finer than {base}."
        )
    times = meta["timepoints"]
    if not times or times != list(range(len(times))):
        raise ValueError("This lesson expects contiguous timepoints starting at frame zero.")
    expected = tuple((int(n) + base - 1) // base for n in meta["source_shape_zyx"])
    ratio = factor // base
    result_shape = tuple((n + ratio - 1) // ratio for n in expected)
    channels = []
    for c in (0, 1):
        volumes = []
        for t in times:
            path = image_path(folder, c, t)
            with tifffile.TiffFile(path) as tf:
                if tf.series[0].shape != expected or tf.series[0].dtype != np.dtype("uint16"):
                    raise ValueError(
                        f"Unexpected shape or dtype in {path.name}; expected uint16 {expected}."
                    )
            task = delayed(read_volume)(path, ratio)
            volumes.append(da.from_delayed(task, shape=result_shape, dtype=np.uint16))
        channel = da.stack(volumes)
        channels.append(channel if lazy else channel.compute(scheduler="single-threaded"))
    spacing = meta.get("voxel_size_um") or 1
    return channels, (1, factor * spacing, factor * spacing, factor * spacing), meta


def _validate_coords(coords, shape):
    if not np.isfinite(coords).all():
        raise ValueError("Coordinates must be finite numbers.")
    if np.any(coords[:, 0] != np.floor(coords[:, 0])) or np.any(coords[:, 0] < 0):
        raise ValueError("Time must be a nonnegative integer frame index.")
    # Pixel centers can extend half a voxel beyond the first/last center.
    if np.any(coords[:, 1:] < -0.5) or np.any(coords[:, 1:] >= np.asarray(shape) - 0.5):
        raise ValueError("Particle or track coordinates are outside the source image bounds.")


def load_tables(folder, metadata):
    """Read precomputed detections and tracks; filter to the loaded timepoints.

    Coordinates remain in the SOURCE grid even for downsampled images.
    Tracks on Zenodo are a numeric CSV without a header, ordered id,t,z,y,x.
    """
    folder = Path(folder)
    detections = pd.read_csv(folder / "detections.csv")
    columns = ["t", "z", "y", "x"]
    if not set(columns).issubset(detections.columns):
        raise ValueError("Detections CSV requires columns t,z,y,x.")
    tracks = np.loadtxt(folder / "tracks.csv", delimiter=",", ndmin=2)
    if tracks.shape[1] != 5:
        raise ValueError("Tracks must have five numeric columns: track_id,t,z,y,x (no header).")
    detections = (
        detections[detections.t.isin(metadata["timepoints"])].copy().reset_index(drop=True)
    )
    tracks = tracks[np.isin(tracks[:, 1], metadata["timepoints"])]
    _validate_coords(detections[columns].to_numpy(), metadata["source_shape_zyx"])
    _validate_coords(tracks[:, 1:], metadata["source_shape_zyx"])
    if (
        np.any(~np.isfinite(tracks[:, 0]))
        or np.any(tracks[:, 0] < 0)
        or np.any(tracks[:, 0] != np.floor(tracks[:, 0]))
    ):
        raise ValueError("Track IDs must be finite nonnegative integers.")
    tracks = tracks[np.lexsort((tracks[:, 1], tracks[:, 0]))]
    if len(tracks) > 1 and np.any(np.all(tracks[1:, :2] == tracks[:-1, :2], axis=1)):
        raise ValueError("A track contains duplicate observations at the same timepoint.")
    return detections, tracks
