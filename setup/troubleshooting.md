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

First close other viewers and memory-heavy applications. Retry the tiny `--gui` setup check. If 2D works but 3D is slow or blank, continue with a 2D slice or maximum-intensity projection and pair with a neighbor for the 3D manipulation. If even 2D napari fails, use the static course page and an instructor demonstration.

Installing the Python packages does not prove that the computer’s graphics driver supports the viewer. Do not spend class time installing random Qt packages or changing display drivers. Record the exact error and machine details for follow-up.

## The data folder is missing or nested twice

The required location is `data/teaching/metadata.json`. If you have `data/teaching/teaching/metadata.json`, move the inner `teaching` folder so there is only one level. If frames are missing, rerun the scripted download or re-extract a complete browser download; do not create blank replacement files.

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

Choose a new name instead of deleting evidence from a previous run:

```console
uv run scripts/render_example.py --data data/teaching --output outputs/example-2
```

After class, compare the folders and remove an unwanted one only after confirming which files you want to keep.
