# Troubleshooting

Start with the symptom you see. Copy the complete error text before closing a window; a screenshot is useful when the error cannot be selected. Record your operating system and, on a Mac, whether the chip is Apple Silicon or Intel.

## `uv` is not found

**Symptom:** PowerShell says “The term 'uv' is not recognized,” or Terminal says `command not found: uv`.

Close every PowerShell or Terminal window, open a new one, and run `uv --version` again. The installer updates the search path for new shells. If it still fails, repeat the installation step from [Windows](windows.md) or [macOS](macos.md). On a managed computer, ask support rather than changing system security settings.

## `pyproject.toml` or `uv.lock` is missing

**Symptom:** `uv sync --locked` says it cannot find the project or lock file.

The terminal is in the wrong folder. On Windows run `Get-Location` and `Get-ChildItem`; on macOS run `pwd` and `ls`. Move into the folder that directly contains both files. Put quotes around a path containing spaces.

## The lock file is out of date

**Symptom:** `uv sync --locked` says the lock needs to be updated.

Do not remove `--locked` and do not generate a new lock during class. You may have mixed files from two workshop versions. Download and extract one complete release into a fresh folder, then rerun the command there.

## The kernel is absent or wrong

In JupyterLab choose **Kernel → Change Kernel… → Python (napari workshop)**. If that choice is missing, stop JupyterLab, move into the workshop folder, and repeat:

```console
uv run python -m ipykernel install --user --name napari-workshop --display-name "Python (napari workshop)"
```

Restart JupyterLab. In the setup notebook, run:

```python
import sys
print(sys.executable)
```

The printed path should contain the current workshop folder and `.venv`. If it points to another Python installation, change the kernel and restart it with **Kernel → Restart Kernel…**.

## The workshop folder was moved or renamed

The named kernel remembers the old `.venv` path. After moving the folder, open a terminal in its new location and run:

```console
uv sync --locked
uv run python -m ipykernel install --user --name napari-workshop --display-name "Python (napari workshop)"
```

Then restart JupyterLab and check `sys.executable` again. If `.venv` was copied from a different computer, remove the copied workshop folder only if you have a safe original, extract a fresh workshop copy, and run `uv sync --locked`; environments are not portable between computers.

## A notebook cell is busy or cells ran out of order

An asterisk such as `[*]` means the kernel is busy. Wait for a normal loading step. If it remains busy, choose **Kernel → Interrupt Kernel** once. For confused variables or cells run out of order, choose **Kernel → Restart Kernel and Run All Cells…**. Save deliberate edits first. Read the first cell that reports an error; later errors may only be consequences.

## Napari does not appear

Napari is a desktop window separate from the JupyterLab browser tab. Check the taskbar or Dock, use **Alt+Tab** on Windows or **Command+Tab** on macOS, and look behind other windows. Keep both the terminal and JupyterLab running.

If no window exists and the notebook reports an error, close other napari windows, restart the kernel, and run the setup notebook in order. From the project folder, also try:

```console
uv run python scripts/check_setup.py --gui
```

Send the instructor the complete terminal output if this fails.

## Qt, OpenGL, graphics, or a blank 3D canvas fails

If the **Practice sphere** layer exists but looks black, first check its contrast limits. The synthetic sphere contains only 0 and 1; set the range to **0–1**. Both setup checks now set that range explicitly. Older copies used the 0–255 default for `uint8`, which made the sphere almost invisible. Once the sphere is visible, drag to check that it rotates.

First close other viewers and memory-heavy applications. Retry the tiny `--gui` setup check. If 2D works but 3D is slow or blank, close the viewer, restart the main notebook kernel, and set `USE_3D = False` in its first code cell. Run from the top. This keeps slices and projections, skips camera rotation, and still exports a PNG and acquired-time movie with projected points/tracks. Pair with a neighbor for the 3D manipulation. If even 2D napari fails, use the static course page and an instructor demonstration.

If the graphics check still fails, record the error and machine details for follow-up after class. Use the 2D or paired option for now; changing Qt packages or display drivers can take time and introduce other problems.

## Windows warnings appear in red, but the notebook continues

A cell can print a warning in red and still finish successfully. A traceback ending in an exception, missing labels, an unusable viewer, or a missing movie needs attention. Keep the complete message; do not disable all warnings.

| Message | What to check and do |
|---|---|
| `QWindowsWindow::setGeometry: Unable to set geometry` | Windows reports different actual and requested window dimensions. Check that the canvas, layer controls, and time slider are visible and usable. Try restoring the window from maximized mode and resizing it within one screen. If controls remain clipped, ask the instructor. Record screen resolution, Windows display scaling, and whether multiple monitors are attached. The cause and workaround still need Windows verification. |
| `DirectWrite: CreateFontFaceFromHDC() failed` mentioning `MS Sans Serif` | Check that `z`/`frame` axis labels, the frame overlay, and controls are readable. If the text is readable and the viewer works, you can continue. We still need to check this on Windows. If text is absent or garbled, stop and show the instructor. Leave font and Qt changes for troubleshooting after class. |
| `IMAGEIO FFMPEG_WRITER WARNING` mentioning `macro_block_size=16` | The encoder is resizing frames for video compatibility. Updated camera and acquired-time examples fit the whole view into 640 × 480 before encoding, so this warning is not expected there. Check that you ran the updated export cells and reopen the movie to inspect its dimensions. Keep the PNGs if encoding fails; do not change `macro_block_size` to hide the warning. |

One Windows reviewer completed the workshop despite these warnings. We still need to test the suggested workarounds on Windows. See the **Windows feedback verification checklist** in the [validation record](../instructor/validation-report.md).

## The data folder is missing or nested twice

The required location is `data/teaching/metadata.json`. If you have `data/teaching/teaching/metadata.json`, move the inner `teaching` folder so there is only one level. If frames are missing or verification reports corrupt files, rerunning the downloader alone will not repair an existing dataset. Preserve it first:

1. Close napari and shut down the notebook kernel so files are not in use.
2. In Finder or File Explorer, rename `data/teaching` to an unused name such as `data/teaching-incomplete`. Keep that folder until the replacement passes verification.
3. From the workshop folder, run `uv run scripts/download_data.py --dataset teaching`. The downloader reuses a checksum-verified `data/downloads/teaching.zip` and extracts a fresh `data/teaching` folder.
4. Rerun the setup notebook one cell at a time. Its complete data check must succeed before continuing.

For a browser download, keep the incomplete folder aside and extract the complete ZIP into a new `data/teaching` folder. Do not create blank replacement files or extract over the incomplete folder.

## A download is slow or interrupted

Rerun the same scripted command. It can reuse data that already pass checksum verification. During class, stop after five minutes and use the instructor’s local copy, paired route, or static 2D material. The full source dataset is optional and should not be downloaded during the core lesson.

## A point or track does not align with the image

Stop and check that images and tables came from the same package. Use the provided loading functions so that the spatial factor is applied consistently. Do not divide coordinates a second time. A teaching package reduced fourfold cannot recreate factor-one detail.

Report the frame, layer names, chosen factor, and a screenshot. Do not “fix” the table by dragging or deleting points; the mismatch may reveal a data or transformation problem.

## Saving is not exporting

**File → Save Notebook** stores code, text, and cell outputs in the `.ipynb` file. It does not create a publication image or movie. A screenshot or movie export is written separately under `outputs/`. Use a new output-folder name for each export because the provided renderer rejects an existing output folder to prevent old and new frames from mixing.

## Movie export fails

Run the setup movie check when instructed:

```console
uv run python scripts/check_setup.py --movie
```

If it fails, keep the PNG screenshot as your result and use the instructor’s reference movie. Record the error rather than installing an unlisted FFmpeg package during class. Playback frames per second changes how quickly the movie plays; it does not establish the biological acquisition interval.

## Memory use is high

Close duplicate viewers and restart the kernel to release arrays. Use the prepared `data/teaching` package and the 2D/projection route. Avoid `--dataset source --timepoints 30` on an 8 GB machine. Lazy loading can limit how many source volumes enter RAM, but the displayed volume still consumes graphics memory and movie export eventually reads every included frame.

## An output folder already exists

Choose a new folder name to keep your earlier exports:

```console
uv run scripts/render_example.py --data data/teaching --output outputs/example-2
```

After class, compare the folders and remove an unwanted one only after confirming which files you want to keep.
