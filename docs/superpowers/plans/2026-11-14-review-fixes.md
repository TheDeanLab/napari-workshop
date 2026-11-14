# Workshop review fixes implementation plan

**Goal:** Fix the six reviewed failures and verify the complete learner workflow.
**Spec:** The six findings in this chat, explicitly accepted for implementation on November 14, 2026.
**Architecture:** Repair existing rendering and notebook paths. Capture the native canvas, then fit it into the export dimensions without cropping. Reuse existing file verification and loaders for setup. Keep the projection scene when 3D is disabled.
**Tech stack:** Locked Python 3.12, napari 0.6.6, NumPy, Pillow, pytest, nbclient, Sphinx.

## Reuse analysis

- Searched source, tests, notebook examples, docs, scripts, exports, and screenshot/resize/verification names.
- Closest symbols: `create_scene`, `export_time_series`, napari `Viewer.screenshot`, `download.verified`, `load_images`, and `load_tables`.
- Repair `create_scene` to synchronize its existing annotation; repair `export_time_series` to capture the native canvas before resizing. Add only the pure `fit_frame(frame, size=(480, 640))` helper for aspect-preserving RGB conversion/padding shared with the notebook; this is an image transformation, not a second screenshot/export lifecycle.
- Compose the existing loaders and `verified` directly in the setup notebook. Do not add a parallel dataset validator or overwrite/repair downloader.
- Reuse the main notebook's projection layers for the fallback rather than introducing another scene builder.
- Document changed public rendering contracts in Numpydoc, update notebook explanations, setup guides, and recovery instructions.

## Constraints and checks

- Preserve source data and exports; use fresh output folders.
- Keep fixed movie dimensions 640 x 480, preserve aspect ratio and entire selected view using black padding.
- Leave the Python/napari versions locked. Declare Pillow directly because the rendering helper imports it (already installed transitively).
- Complete implementation in the managed worktree, with an independent final review.
- Tests must exercise behavior: colored frame borders and aspect ratios; real viewer label changes; malformed/missing/checksum-invalid data through the setup cell; full notebook execution in 3D and with `USE_3D=False`.
- Human prose needs inspection and a warnings-as-errors documentation build, not string-matching tests.

## Tasks

- [x] 1. Add failing rendering and setup-data regressions; record the observed failures.
- [x] 2. Implement `fit_frame`, repair scene labels and exports, update Numpydoc, and synchronize direct dependency locks.
- [x] 3. Replace setup existence checks with header/table/checksum verification; change OS instructions to pause for the graphics check; document moving incomplete data aside.
- [x] 4. Add `USE_3D` to the main lesson, guard both 3D transitions and camera-only animation, preserve projection overlays through PNG and acquired-time export, and update fallback prose.
- [x] 5. Run targeted/full pytest, Ruff, relevant typing checks, notebook format checks, documentation build, all four learner notebooks plus instructor solution, and the main lesson again in 2D. Inspect native/fitted captures and movie dimensions/frame labels.
- [x] 6. Independent final review, address relevant findings, record validation and commit with reuse analysis.

## Review focus

Retina/high-DPI canvas framing; wide and tall aspect ratios; frame labels after manual slider changes and movie export; browser-extracted corrupt/missing data; no 3D or camera animation when `USE_3D=False`; recovery without deleting user files.

## Execution record

- Baseline from prior review: 10 tests, all learner notebooks, lint, formatting, and Sphinx passed; six behavioral/documentation failures were reproduced or traced.

- Regressions before fixes: 8/9 new rendering/setup tests failed for the expected reasons; the added projection-transition test also failed by entering 3D.
- After fixes: all 20 tests passed with GUI tests enabled; Ruff and all five notebook-format checks passed. Two upstream itertools deprecation warnings remain.
- All four learner notebooks and the instructor solution executed in fresh local kernels. The main notebook also passed with USE_3D=False and an assertion rejecting every attempted 3D transition.
- All four acquired-time exports reopened as 30 frames, 5 fps, 640 x 480. Native/fitted screenshots and the frame-10 rotation image were visually inspected.
- Sphinx warnings-as-errors and offline ZIP build passed after correcting two new section links.
- Scoped basedpyright retains the same six pre-existing pandas/ImageIO inference/stub errors as the original render module; the new generic return annotation was corrected. This repo has no configured type-checking gate.
- Independent read-only reviewer approved all six fixes with no findings. Platform GPU reliability beyond this Apple Silicon machine, human learner usability, and live network availability remain outside this local verification; the prior review verified the teaching download.
- Ruling: retain the existing downloader's no-overwrite behavior and correct recovery prose, preserving incomplete data rather than silently replacing it.
- Ruling: retain current pinned dependency versions; Pillow was already installed transitively and is now declared directly. The lockfile writer updated its format revision.
