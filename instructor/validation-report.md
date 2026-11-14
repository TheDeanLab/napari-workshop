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

## November 14, 2026: learner feedback fixes

Validated on the same Apple Silicon/macOS environment listed above. Five new
regression cases failed before the fix and passed afterward: both actual sphere
entry points must render bright pixels, and all three notebook camera-export
paths must preserve the full native frame at 640 × 480 without an encoder resizing
warning. The encoding cases use a non-multiple-of-16 synthetic canvas with edge
features; separate notebook runs exercise the real napari-animation interpolation.

Verification commands and outcomes:

| Check | Result |
|---|---|
| `NAPARI_WORKSHOP_GUI_TESTS=1 uv run pytest -q` | 25 passed, including five desktop cases; two upstream Python `itertools` deprecation warnings. |
| `uv run ruff check src tests scripts docs/conf.py` | Passed. |
| `uv run ruff format --check src tests scripts docs/conf.py` | Passed; 17 Python files checked. |
| `uv run python scripts/check_setup.py --movie` | Encoder wrote and read three frames. |
| `nbformat.validate` on all four learner notebooks and instructor solution | Passed; source notebooks retain empty outputs/execution counts. |
| Fresh-kernel notebook execution | All four learner notebooks, instructor solution, and main lesson with `USE_3D = False` passed. |
| `uv run --group docs python scripts/build_handouts.py` | HTML and offline ZIP built successfully with Sphinx warnings treated as errors. |

Each kernel used this worktree's Python environment. Additional validation cells
checked the visible sphere, particle sizes across acquisition frames, the 2D route
remaining in 2D, and decoded movie properties. The three camera movies contained
31 frames at 10 playback fps; four acquired-time movies contained 30 frames at
5 fps. All seven movies were 640 × 480; first and last frames differed. Camera
first-frame pixels were compared with the fitted native PNGs. The bright sphere
and representative decoded first/last camera views were visually inspected.
No reported Qt/font or encoder-resizing warning occurred in these Mac notebook
runs. This is not evidence that the Windows Qt/font issues are resolved.

Local executed notebooks, the sphere screenshot, and movie verification records
are retained in `outputs/feedback-verification-20261114/`; their JSON records name
the corresponding fresh export directories. Generated outputs are not committed.
The original setup notebook execution check had missed the dark sphere: completing
cells did not establish that the practice object was visible. The new desktop
regression tests explicitly cover that failure. An independent code review found
no additional actionable issues.

## Windows feedback verification checklist

The November reviewer reported completing the Windows workshop despite a blank
practice sphere, point-size confusion, and Qt/font/video warnings. They did not
test macOS. Assaf specifically flagged the sphere because it occurs at the start.
The feedback is a learner report, not a controlled platform qualification.

The sphere failure was reproduced on Apple Silicon: the synthetic `uint8` image
contains values 0 and 1, while napari's default contrast range is 0–255. Explicit
limits of 0–1 restore the sphere in both setup entry points. Camera movies now
compose napari-animation's supported PNG-directory export with `fit_frame` and
ImageIO encoding at 640 × 480. Native PNGs remain in `camera-frames` for inspection.
The particle-size exercise changes all existing points through `particles.size`;
GUI selection is explained separately as affecting selected visible points.

**Still unverified on Windows:** complete the following on a physical Windows
laptop using the revised course files. Do not mark Qt/font warnings resolved from
macOS tests or from non-GUI CI alone.

- Record the course commit/archive, Windows version, CPU, RAM, GPU/driver, screen
  resolution, display scaling, monitor count, and package versions printed by
  `uv run python scripts/check_setup.py --movie`.
- Follow the course-ZIP instructions from a fresh extraction. Confirm the selected
  ZIP contains `pyproject.toml`, `uv.lock`, `notebooks`, and `scripts`; the offline
  handouts ZIP is not the runnable course. Published v0.1.1 downloads predate these
  fixes, so distribute a revised archive before testing them.
- Run `uv run python scripts/check_setup.py --gui`, then the setup notebook one
  cell at a time. In each, confirm the sphere is visibly bright and rotates, then
  close it. Retain a screenshot and any warning text.
- Open the main notebook at the laptop's normal display scaling. If
  `QWindowsWindow::setGeometry` appears, confirm that all layer controls, the
  canvas, and time/z sliders remain accessible. Try restoring/resizing within one
  screen and record whether that changes the warning or clipping. Repeat on an
  external monitor if that is part of the intended classroom setup. This suggested
  workaround has not been verified here.
- Inspect `z`/`frame` axis labels, the frame overlay, and controls in notebooks 01,
  02, and 03. If `DirectWrite: CreateFontFaceFromHDC()` mentioning `MS Sans Serif`
  appears, record whether the text is readable or missing/garbled. No font
  substitution or warning suppression has been introduced; its Windows cause and
  any required font correction remain unresolved.
- Run the particle-size cell and compare frames 0 and 10. Test the documented GUI
  selection procedure separately, confirming it affects only selected points and
  that returning to Toggle Camera restores navigation.
- Run main and optional camera exports from a non-square window. Verify 31 frames,
  10 playback fps, and 640 × 480 pixels, with full framing and no
  `macro_block_size` resizing warning. Play the MP4 in the normal Windows player
  and compare first/last views with the retained PNGs. Acquired-time movies should
  contain 30 frames at 5 fps and the same dimensions.
- Restart the main notebook with `USE_3D = False`; verify projection, particles,
  tracks, PNG, and acquired-time MP4 work and camera rotation is skipped.

Record each outcome as pass/fail/not tested, with the exact warning and artifact
path. If labels or controls are unusable, use the documented fallback and retain
the failure for investigation. A warning-free Mac run does not settle these two
Windows Qt issues. The timed novice rehearsal, Intel Mac pilot, and 8 GiB laptop
target also remain unverified.
