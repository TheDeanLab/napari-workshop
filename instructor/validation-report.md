# Validation record

Validation performed on September 10, 2026. This report separates observed checks from platform pilots still needed.

## Source and teaching data

The public [Zenodo record 22694247](https://doi.org/10.5281/zenodo.22694247) contains 60 TIFF stacks, two CSV tables, and a MATLAB metadata file. All 60 source images and both tables matched the pinned Zenodo sizes and checksums before preparation. The first original frame from both channels and both tables were also downloaded over HTTPS through the course downloader; lazy factor-4 reduction reproduced the prepared first-frame image values exactly.

The teaching archive contains both channels and all 30 frames at factor 4, 28,105 supplied detections, and 25,076 track rows representing 2,058 IDs. Its exact ZIP size is 42,810,555 bytes; its SHA-256 is pinned in `data/teaching-manifest.json`. The reduced image shape is `30 × 166 × 215` in `z,y,x`; all image arrays together occupy 122.5 MiB. The prepare command was rerun into separate destinations after the failure-recovery revision. All 62 resulting TIFF/CSV files reproduced byte-for-byte with the final locked preparation environment. ZIP extraction and reuse checks passed.

## Runtime and notebooks

Nine targeted automated tests passed. They cover lazy reads, eager/lazy agreement, source-coordinate preservation including nondivisible dimensions and edge points, missing frames, unavailable finer resolution, table bounds/filtering, checksum protection, interrupted downloads, safe archive extraction, and failed preparation cleanup.

All four learner notebooks executed from fresh Jupyter kernels with the prepared data. Both animation examples produced movies. The main workshop uses real image, detection, and track layers. Reference PNGs and the MP4 were generated from these data and inspected. The source notebooks ship without machine-specific output cells.

The Linux environment used Python 3.12, napari 0.6.6, NumPy 2.2.6, PyQt6 6.11.0, and imageio-ffmpeg 0.6.0. These versions are locked in the course environment; napari is deliberately pinned to the tested course API.

A separate 30-frame, 640 × 480 MP4 exported at 10 playback fps and reopened with the expected frame count and dimensions. The first and last frames differed. The complete render command took 15.43 seconds and peaked at 790,416 KiB (about 772 MiB) resident process memory on this Linux host using Mesa software OpenGL. This is evidence for this bounded render only; it does not measure total desktop memory, student GPU capacity, or laptop performance.

## Documentation and portability

The HTML walkthrough builds with Sphinx warnings treated as errors. The offline ZIP includes the same pages, notebook downloads, reference images, and reference MP4. The documentation build never executes Qt notebooks.

GitHub Actions checks the locked environment, tests, encoder, notebook format, and lint on Linux, Windows, and macOS. Consult the [runtime workflow](https://github.com/TheDeanLab/napari-workshop/actions/workflows/tests.yml) for the exact commit and outcomes. CI checks do not exercise interactive Qt/OpenGL.

## Remaining instructor checks

- Run the full learner path on a Windows laptop, an Apple Silicon Mac, and an Intel Mac, recording RAM, OS, graphics behavior, and MP4 playback.
- Rehearse the 180-minute schedule with a biologist unfamiliar with the notebook; the timetable is an instructional plan, not a measured novice completion time.
- Confirm particle identity, voxel calibration, and acquisition timing. Until then, the materials intentionally use source voxels and frame indices.

Eight GiB RAM is a target for the prepared data, and 16 GiB is preferred. Neither has been certified by a completed laptop pilot. Keep the documented 2D, paired, and static fallback routes available.

## v0.1.1: published teaching DOI

The [teaching derivative record 22696913](https://doi.org/10.5281/zenodo.22696913) was verified after publication on September 10, 2026. A fresh HTTPS download matched both Zenodo’s MD5 and the existing release SHA-256; extraction validated the per-file checksums. The archive remains 42,810,555 bytes and is byte-identical to the original GitHub mirror. Existing verified downloads were successfully reused.

The default downloader now uses the teaching record, while original-resolution downloads still use record 22694247. Both DOIs appear in the course citations. A preparation regression test confirms that generating a candidate archive cannot overwrite the published download manifest. All ten targeted tests passed locally. Notebook code and runtime dependencies are unchanged from v0.1.0; notebook citations, online pages, and downloadable handouts were refreshed.


## November 14, 2026: review fixes and Apple Silicon execution

The six review fixes were validated on macOS 26.7.3, Apple Silicon, 48 GiB RAM,
Python 3.12.11, napari 0.6.6, and PyQt6 6.11.0 with a Retina display (pixel ratio 2).
Exports now capture the native canvas and fit the complete view into 640 × 480
pixels with aspect-preserving black padding. Shared scenes synchronize their frame
annotation. Setup checks every TIFF header, both tables, and all teaching-file
checksums; the OS guides require a pause for graphics inspection. The main lesson's
`USE_3D = False` route retains projection overlays through export and skips camera
rotation. Recovery instructions preserve incomplete data before fresh extraction.

All 20 tests passed, including three desktop rendering tests. To run those tests
on a machine with working Qt/OpenGL, set `NAPARI_WORKSHOP_GUI_TESTS=1` before
running `uv run pytest -q`; otherwise the three GUI tests are skipped. Two upstream
Python `itertools` deprecation warnings were emitted. Ruff lint/format checks and
all five notebook-format checks passed. The HTML/offline ZIP build passed with
Sphinx warnings treated as errors.

All four learner notebooks and the instructor solution ran in fresh kernels.
The main lesson also ran completely with `USE_3D = False`, with verification that
no cell attempted to enter 3D. Each acquired-time movie reopened as 30 frames at
5 playback fps and 640 × 480 pixels. PNG framing and the corrected frame-10
camera-animation annotation were visually inspected. Camera movies contained
31 rendered views at 10 playback fps; those interpolated views are not additional
acquired timepoints.

A scoped optional `basedpyright` check still reports the same six pre-existing
pandas/ImageIO inference or stub errors in the rendering module as the original
revision; type checking is not a configured repository gate. No new type errors
remain from these changes. An independent code review found no additional issues.

This establishes automated execution and export on this Apple Silicon machine.
It does not certify learner interaction, an 8 GiB memory target, Windows, or Intel
macOS. Those platform and novice-learner pilots remain outstanding.
