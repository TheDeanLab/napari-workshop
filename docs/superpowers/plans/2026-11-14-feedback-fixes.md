# Workshop feedback fixes implementation plan

> Execute inline using the debugging, test-driven-development, and verification skills.

**Goal:** Resolve the confirmed learner feedback and record the Windows checks that cannot be performed on this Mac.

**Architecture:** Keep the existing notebook workflows and pinned dependencies. Set explicit sphere contrast. Compose napari-animation's supported PNG export with the existing `fit_frame` and ImageIO encoder; retain intermediate PNGs for inspection.

**Spec:** User-authorized fixes for the feedback in [napari Workshop Overview](https://docs.google.com/document/d/1qnH7qmew5iq-AKDUb_VD3ml0zOdpX7ituCph8zGbH3g/edit).

## Reuse analysis

- Searched source, tests, notebook examples, instructor solution, exports, and animation/frame/movie synonyms. Closest symbols are `fit_frame`, `export_time_series`, `Animation.animate`, and `Animation.set_movie_frame_index`.
- Reuse `fit_frame` and the supported `Animation.animate` extensionless PNG-directory output. Encode those frames in notebook cells using the same ImageIO settings as acquired-time movies.
- No new user-callable API: a camera-export wrapper would duplicate existing export lifecycle; manual interpolation/frame counting would duplicate napari-animation. The PNG stage costs bounded disk space for the short exercise but preserves public APIs and avoids private plugin state.
- Synchronize the main, optional, and instructor examples and explain retained PNGs. No dependency changes.

## Constraints and review focus

- Preserve source data and prior outputs; use fresh output directories.
- Sphere validation must check visible pixels, not merely a successful import.
- Camera export must preserve full framing on non-multiple-of-16/high-DPI canvases, include the final keyframe, and reopen as 640 × 480 at 10 fps.
- Point-size instructions must distinguish all-frame changes from selected visible points; preserve cell IDs and use those IDs in tests when adding the exercise cell shifts indices.
- Keep the 2D fallback executable; do not hide Qt warnings or claim Windows verification.
- Existing published release ZIPs are immutable artifacts; local changes require a subsequent release before those downloads contain these fixes.

## Tasks

- [x] Add and run failing regression tests for both sphere entry points and the three camera-export cells.
- [x] Fix sphere contrast and reuse frame fitting in the three camera movies; run targeted tests.
- [x] Clarify ZIP selection, introduce terms before setup, correct point-size exercise, and add symptom-specific warning guidance.
- [x] Run full tests with GUI enabled, Ruff, notebook validation, encoder check, and documentation build.
- [x] Execute all four learner notebooks, instructor solution, and main 2D fallback in fresh kernels; inspect sphere and decoded camera artifacts.
- [x] Record results and concrete Windows verification steps; review final diff.

## Results

All 25 tests passed, including five GUI cases. The five feedback regressions failed on the original code and passed after correction. All six fresh-kernel notebook runs passed; all seven decoded movies had expected frame counts, fps, and 640 × 480 dimensions. The sphere and representative camera views were visually checked. Ruff, clean notebook format, encoder, and Sphinx/offline ZIP checks passed. Independent review found no actionable issues. See `instructor/validation-report.md` for evidence and the remaining Windows checklist.

Implementation adjustment: the particle exercise warranted its own executable cell. The existing 2D regression now finds its scene cells by stable IDs rather than numeric positions; this preserves its coverage when prose or exercises are inserted.
