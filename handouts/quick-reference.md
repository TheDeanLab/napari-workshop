# Workshop quick reference

Keep this page beside you during the workshop.

## Start and stop

Open PowerShell (Windows) or Terminal (macOS), move into the workshop folder, then:

```console
uv sync --locked
uv run jupyter lab
```

Open `notebooks/01_rendering_workshop.ipynb`. Select **Python (napari workshop)** at the upper right. JupyterLab is in the browser; napari is a separate window. To finish, save the notebook, close napari, then choose **File → Shut Down** in JupyterLab.

## Where things are

| Item | Location |
|---|---|
| Main lesson | `notebooks/01_rendering_workshop.ipynb` |
| Setup check | `notebooks/00_check_setup.ipynb` |
| Teaching data | `data/teaching/` |
| Screenshots and movies | `outputs/` |
| Help | `setup/troubleshooting.md` |

## Notebook controls

| Goal | Action |
|---|---|
| Run selected cell | **Shift+Enter** |
| Run from a clean state | **Kernel → Restart Kernel and Run All Cells…** |
| Stop a stuck cell | **Kernel → Interrupt Kernel** |
| Confirm Python | Run `import sys; print(sys.executable)`; path should contain this folder and `.venv` |
| Save code and notes | **File → Save Notebook** |

Run cells from top to bottom. `[*]` means Python is busy; a number such as `[7]` means the cell finished.

## Napari controls

| Goal | Action |
|---|---|
| Select a layer | Click its name in the layer list |
| Show/hide a layer | Click its eye icon |
| Change contrast | Adjust **contrast limits** for the selected image layer |
| Change color | Select a **colormap** |
| Combine light from layers | Set image **blending** to `additive` and adjust opacity |
| Move through time/depth | Drag the `t` or `z` dimension slider |
| Switch 2D/3D | Click the 2D/3D display button |
| Pan | Drag with the pan/zoom tool |
| Zoom | Mouse wheel or trackpad scroll |
| Reset view | Press **Home** |

Display controls change what you see, not the stored voxel intensities. A maximum-intensity projection keeps the brightest value along depth and discards where that value was along `z`.

## Coordinates and meaning

- Images, detections: `t, z, y, x`
- Tracks: `id, t, z, y, x`
- `t` is a frame index from 0 to 29, not confirmed seconds.
- Spatial coordinates are source voxels, not confirmed micrometres.
- A point is a supplied candidate detection.
- A track is a supplied association of detections across frames.
- Track tail length is a time window; it is not the number of particles.
- The prepared data are reduced fourfold in space, so fine detail is lost.

## Recovery

- No napari window: look behind the browser or use **Alt+Tab/Command+Tab**.
- Wrong result: restart the kernel and run all cells in order.
- Missing data: confirm `data/teaching/metadata.json` exists.
- Slow/blank 3D: use the 2D or projection route and pair for the 3D activity.
- Movie fails: keep the PNG screenshot and use the reference movie.
- Download exceeds five class minutes: use the instructor’s local copy or paired route.
- Existing output folder: choose a new output name; do not mix old and new frames.

Teaching dataset: <https://doi.org/10.5281/zenodo.22696913>. Original source: <https://doi.org/10.5281/zenodo.22694247>. Both CC BY 4.0.
