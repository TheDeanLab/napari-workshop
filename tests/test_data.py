"""Catch coordinate drift, missing frames, and unintended eager reads."""

import json

import numpy as np
import pandas as pd
import pytest
import tifffile


def test_lazy_matches_eager_and_preserves_source_coordinate_scale(dataset, monkeypatch):
    from napari_workshop.data import load_images, load_tables

    reads = []
    original = tifffile.imread

    def counted(*args, **kwargs):
        reads.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(tifffile, "imread", counted)
    images, scale, meta = load_images(dataset, downsample=2, lazy=True)
    assert reads == []
    assert images[0].shape == (2, 4, 4, 4)
    assert scale == (1, 2, 2, 2)
    a = images[0][0].compute(scheduler="single-threaded")
    assert len(reads) == 1
    assert np.unravel_index(a.argmax(), a.shape) == (2, 2, 2)
    eager, _, _ = load_images(dataset, downsample=2, lazy=False)
    np.testing.assert_array_equal(a, eager[0][0])
    points, tracks = load_tables(dataset, meta)
    assert points.loc[0, "x"] == 4
    assert tracks[0].tolist() == [7, 0, 4, 4, 4]


def test_reduced_package_cannot_recover_finer_resolution(dataset):
    from napari_workshop.data import load_images

    meta = json.loads((dataset / "metadata.json").read_text())
    meta["spatial_factor"] = 4
    (dataset / "metadata.json").write_text(json.dumps(meta))
    with pytest.raises(ValueError, match="resolution|factor"):
        load_images(dataset, downsample=2)


def test_missing_channel_frame_is_reported_before_loading(dataset):
    from napari_workshop.data import load_images

    (dataset / "ch1/frame_000001.tif").unlink()
    with pytest.raises((FileNotFoundError, ValueError), match="frame|timepoint"):
        load_images(dataset)


def test_tables_validate_bounds_and_filter_selected_times(dataset):
    from napari_workshop.data import load_tables

    meta = json.loads((dataset / "metadata.json").read_text())
    meta["timepoints"] = [0]
    points, tracks = load_tables(dataset, meta)
    assert len(points) == len(tracks) == 1
    a = pd.read_csv(dataset / "detections.csv")
    a.loc[0, "x"] = 999
    a.to_csv(dataset / "detections.csv", index=False)
    with pytest.raises(ValueError, match="bound"):
        load_tables(dataset, meta)


def test_nondivisible_grid_keeps_sampled_centers_and_source_edge_points(dataset):
    from napari_workshop.data import load_images, load_tables

    shape = (9, 10, 11)
    for channel in (0, 1):
        for t in range(2):
            array = np.zeros(shape, dtype=np.uint16)
            array[8, 8, 8] = 1000
            tifffile.imwrite(dataset / f"ch{channel}/frame_{t:06d}.tif", array)
    meta = json.loads((dataset / "metadata.json").read_text())
    meta["source_shape_zyx"] = list(shape)
    (dataset / "metadata.json").write_text(json.dumps(meta))
    points = pd.read_csv(dataset / "detections.csv")
    points.loc[0, ["z", "y", "x"]] = [-0.49, -0.49, -0.49]
    points.loc[1, ["z", "y", "x"]] = [8.49, 9.49, 10.49]
    points.to_csv(dataset / "detections.csv", index=False)
    images, scale, meta = load_images(dataset, downsample=4)
    volume = images[0][0].compute(scheduler="single-threaded")
    assert volume.shape == (3, 3, 3)
    assert tuple(np.asarray(np.unravel_index(volume.argmax(), volume.shape)) * scale[1:]) == (
        8,
        8,
        8,
    )
    retained, _ = load_tables(dataset, meta)
    np.testing.assert_array_equal(retained[["z", "y", "x"]], points[["z", "y", "x"]])
    # Display cells may differ from the source footprint; centers are not stretched.
    coarse_edges = (np.asarray(volume.shape) - 0.5) * np.asarray(scale[1:])
    assert np.all(np.abs(coarse_edges - (np.asarray(shape) - 0.5)) < 2)
