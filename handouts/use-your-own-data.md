# Use your own data

Once you can run the workshop example, try it with a small sample of your own data. Copy the notebook within the workshop folder, and keep your original data files unchanged. The steps below describe the file formats and adjustments the workshop helpers need.

## 1. Check whether your data fit the lesson

The workshop expects two image channels with axes in this order:

```text
t, z, y, x
```

Each timepoint must have the same `z,y,x` shape and dtype within a channel. Frame identifiers must sort in acquisition order. A single 3D volume can be treated as one timepoint. A 2D time series uses `t,y,x` and needs the 2D route described below.

Do not guess axis order from the picture. Read TIFF metadata or ask the person who produced the files. A plausible-looking transposed image can still place overlays incorrectly.

## 2. Record units before plotting

Write down, from acquisition metadata:

- voxel spacing for `z`, `y`, and `x`, with units;
- acquisition timestamps or the interval between frames;
- channel names and what evidence supports their biological interpretation;
- any crop, binning, resampling, or coordinate offset already applied.

If a value is unknown, keep spatial values in voxels and time as frame indices. You will need the missing calibration before reporting physical distances or speeds. The workshop example also uses voxels and frame indices while we confirm its calibration.

## 3. Prepare the tables

A detections table must have a header with at least:

```text
t,z,y,x
```

Additional columns such as `amp` or `int` may be retained as measurements, but their interpretation should be documented.

A tracks table uses:

```text
track_id,t,z,y,x
```

Napari expects the identifier first. The course helper requires a **headerless numeric** `tracks.csv` in `id,t,z,y,x` order; it reads values with `numpy.loadtxt`. A file beginning with `track_id,t,z,y,x` will fail in that helper. For an independently written loader, a header is useful: read it with pandas and explicitly select columns in napari order. Document whether positions are array indices, source voxels, display-array coordinates, or physical coordinates.

Before display, verify that every `t` and spatial coordinate lies within the corresponding image bounds. Keep a separate record of any excluded or unmatched rows and why you left them out. Check the tracks against the images for incorrect links.

## 4. Use relative paths

Keep the complete workshop folder, including its environment and source code. The copied notebook locates that root using `data/zenodo-manifest.json`; an unrelated folder with only a notebook is insufficient. Add your small dataset alongside the course data:

```text
napari-workshop/
├── pyproject.toml, uv.lock, src/, scripts/
├── notebooks/my-rendering.ipynb
├── data/
│   ├── zenodo-manifest.json
│   ├── teaching/
│   └── my-data/
│       ├── metadata.json
│       ├── ch0/frame_000000.tif, frame_000001.tif, ...
│       ├── ch1/frame_000000.tif, frame_000001.tif, ...
│       ├── detections.csv
│       └── tracks.csv
└── outputs/
```

To reuse `load_images` and `load_tables`, both channels must contain unsigned 16-bit (`uint16`) ZYX stacks with these exact names and contiguous frames starting at zero. The CSV requirements above also apply. Write `metadata.json` to describe **your** arrays, for example for two unreduced volumes of shape `(20, 64, 64)` per channel:

```json
{
  "spatial_factor": 1,
  "source_shape_zyx": [20, 64, 64],
  "timepoints": [0, 1],
  "coordinate_system": "source_voxels",
  "voxel_size_um": null,
  "time_step_s": null
}
```

Replace the shape and timepoints with measured values. A reduced dataset must record its actual reduction factor and original shape; the helper assumes the course’s sample-at-zero convention. Keep null calibration values when using source-voxel coordinates. This helper does not implement arbitrary TIFF layouts, crops, anisotropic physical scaling, or channel counts. Those need an explicitly adapted loader and layer transforms; do not change metadata merely to make an incompatible file pass.

Set the copied notebook’s data path to `ROOT / "data/my-data"`. Relative paths allow the whole course folder to move together. Avoid a path that names one person’s Desktop or home folder.

## 5. Estimate image memory

For an uncompressed in-memory array:

```text
bytes = t × z × y × x × bytes per voxel × number of channels
```

`uint16` uses 2 bytes per voxel. Divide bytes by `1024³` for GiB. For example, the complete workshop source images require:

```text
30 × 118 × 664 × 860 × 2 × 2 ≈ 7.53 GiB
```

This excludes projections, copies, tables, Python, the operating system, and graphics memory. Do not plan to fill all available RAM. Test one timepoint first and watch actual memory on the least capable target computer.

## 6. Choose a loading route

| Route | Appropriate when | Main limitation |
|---|---|---|
| Small eager array | The full prepared array comfortably fits RAM | Loads and holds the complete array |
| 2D or projection | The question can be answered without full depth | Projection discards depth; a slice omits other planes |
| Lazy source stack | Many separate source volumes are too large to hold together | Each requested chunk still takes time; displayed data still use GPU memory |
| Spatially reduced copy | Fine detail is not required for the teaching question | Lost detail cannot be recovered |

Lazy loading and downsampling solve different problems. Downsampling after opening a compressed stack may still require reading that stack. Lazy loading does not shorten a prior download. Never call whole-series `compute()`, `persist()`, or `numpy.asarray(...)` on a dataset that does not fit memory.

## 7. Keep images and overlays aligned

Apply coordinate transforms once. If an image was cropped, account for its source offset. If it was reduced, use the documented resampling convention. Then either transform the table coordinates or give image, points, and tracks matching layer `scale` and `translate` values.

Check several recognizable objects at early, middle, and late frames. Verify each supported reduction factor separately. A package already reduced by factor 4 can be displayed at factor 4 or coarser; it cannot recover factors 1 or 2 from absent pixels.

## 8. Adapt a copy of the notebook

1. Duplicate `notebooks/01_rendering_workshop.ipynb` and rename the copy.
2. Check that your files meet the format requirements above, then change the data path and layer names.
3. Adjust example indices such as `z_plane = 15` and frame 10 to valid positions in your smaller dataset; update any fixed frame counts or contrast settings.
4. Run from a restarted kernel and confirm shapes, axes, and table bounds.
5. Add one image layer at a time, then points, then tracks.
6. Use a new output folder for each export.
7. Record data identity, transforms, package versions, and limitations beside the result.

Do not copy display parameters and biological captions without checking them on the new specimen. Contrast settings, particle size, tail length, and camera angle affect communication, while detection and tracking validity require their own analysis outside this workshop.

## 2D fallback

For `t,y,x` images, omit `z` from points and tracks so points use `t,y,x` and tracks use `track_id,t,y,x`. For a maximum-intensity projection of 3D data, remove `z` only after computing the projection and document that depth was discarded. Do not leave a dummy `z` column and assume napari will ignore it.
