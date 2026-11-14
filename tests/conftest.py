"""Small real TIFF dataset shared by data and rendering regressions."""

import json

import numpy as np
import pandas as pd
import pytest
import tifffile


@pytest.fixture
def dataset(tmp_path):
    for c in (0, 1):
        folder = tmp_path / f"ch{c}"
        folder.mkdir()
        for t in range(2):
            a = np.zeros((8, 8, 8), dtype=np.uint16)
            a[4, 4, 4] = 1000 + t
            tifffile.imwrite(folder / f"frame_{t:06d}.tif", a, metadata={"axes": "ZYX"})
    (tmp_path / "metadata.json").write_text(
        json.dumps(
            {
                "spatial_factor": 1,
                "source_shape_zyx": [8, 8, 8],
                "timepoints": [0, 1],
                "coordinate_system": "source_voxels",
                "voxel_size_um": None,
                "time_step_s": None,
            }
        )
    )
    pd.DataFrame(
        {
            "t": [0, 1],
            "z": [4.0, 4.0],
            "y": [4.0, 4.0],
            "x": [4.0, 4.0],
            "amp": [10.0, 11.0],
            "int": [10.0, 11.0],
        }
    ).to_csv(tmp_path / "detections.csv", index=False)
    np.savetxt(tmp_path / "tracks.csv", [[7, 0, 4, 4, 4], [7, 1, 4, 4, 4]], delimiter=",")
    return tmp_path
