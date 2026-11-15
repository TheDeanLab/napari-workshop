# macOS setup

Complete this setup before class if you can. You need an internet connection, permission to install software for your account, and about 10 GB of free space. Use the same course files for Apple Silicon and Intel Macs.

Before typing commands, here are the tools you will use:

- **Python environment:** the workshop’s own Python and installed packages, stored in `.venv` so they stay together.
- **Terminal / PowerShell:** the command window where you install packages and start JupyterLab.
- **JupyterLab:** the application that opens a notebook in your browser. A notebook contains explanations and code cells.
- **Kernel:** the running Python process that executes those cells and remembers their variables. Select **Python (napari workshop)**. Restarting it clears those variables.
- **Napari:** the separate desktop window where you view and manipulate images and layers.

Keep the terminal running while you use JupyterLab and napari. More terms are in the [glossary](../handouts/glossary.md).

## 1. Identify your Mac and open Terminal

Choose **Apple menu → About This Mac**. Record the macOS version and chip:

- **Apple M1, M2, M3, M4, or later** means Apple Silicon.
- **Intel** in the processor name means an Intel Mac.

This information helps diagnose package or movie-export problems. Next open **Finder → Applications → Utilities → Terminal**. A line ending in `%` or `$` is the prompt. Type only the command itself, then press **Return**.

If your organization manages the Mac and blocks installation, stop and contact its support staff or the workshop instructor. You should not need `sudo` for this setup.

## 2. Install uv

`uv` installs Python and the packages recorded for the workshop. Copy the following command from the [official uv installation page](https://docs.astral.sh/uv/getting-started/installation/), paste it into Terminal, and press **Return**:

```console
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`curl` downloads the official installer, and `sh` runs it. Close Terminal, reopen it, and check the installation:

```console
uv --version
```

Success looks like `uv 0.x.y` (the numbers may differ). If Terminal says `command not found`, close every Terminal window and try once more, then see [troubleshooting](troubleshooting.md).

## 3. Download and extract the workshop folder

Download the **course files**, [`napari-workshop-v0.1.3.zip`](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.3/napari-workshop-v0.1.3.zip). This release includes the revised documentation and the November setup and rendering fixes. Extract it into a fresh folder rather than mixing it with an older course copy.

| ZIP file | Purpose |
|---|---|
| `napari-workshop-v0.1.3.zip` | Required: notebooks, scripts, and Python environment files. Extract this as your workshop folder. |
| `napari-workshop-handouts.zip` | Optional: offline reading in a browser. It cannot replace the course files. |
| `teaching.zip` | Microscopy data, downloaded separately in the data step below. |

Safari normally expands a ZIP automatically in **Downloads**. If it does not, double-click the ZIP in Finder.

Move the resulting folder to **Documents**. Open it and confirm that it directly contains `README.md`, `pyproject.toml`, `uv.lock`, `notebooks`, and `scripts`. GitHub may name it `napari-workshop-main`; that name is fine.

## 4. Move Terminal into the folder

Type `cd` followed by one space, drag the extracted folder from Finder into Terminal, and press **Return**. Dragging inserts the exact path and safely handles spaces. Then list the folder:

```console
pwd
ls
```

`pwd` prints your current folder. `ls` should show `pyproject.toml`, `uv.lock`, `notebooks`, and `scripts`. If it does not, locate the folder that directly contains those files.

An equivalent typed command is below; quotation marks keep a path with spaces together:

```console
cd "$HOME/Documents/napari-workshop-main"
```

## 5. Create the workshop environment

```console
uv sync --locked
```

`uv sync` creates a private `.venv` environment inside this workshop folder and installs its packages. `--locked` requires the tested versions recorded in `uv.lock`. uv may first download Python 3.12. The first run can take several minutes.

Success ends without red error text and leaves a hidden `.venv` folder. You do not need to activate it. Register this environment as a Jupyter kernel:

```console
uv run python -m ipykernel install --user --name napari-workshop --display-name "Python (napari workshop)"
```

This uses Python from `.venv` and creates the kernel choice **Python (napari workshop)**. Success includes a message beginning `Installed kernelspec`.

## 6. Download and check the data

Follow [Download the data](download-data.md). The recommended command is:

```console
uv run scripts/download_data.py --dataset teaching
```

Run the non-graphical checks:

```console
uv run python scripts/check_setup.py
```

Success lists a Python executable inside this workshop’s `.venv`, napari 0.6.6 and other package versions, available RAM, and `Checks complete`. The exact folder and RAM number vary by computer.

Then test a tiny napari window:

```console
uv run python scripts/check_setup.py --gui
```

A separate napari window should appear. Close it after the test. Add `--movie` only when the instructor asks you to test movie export. If macOS asks whether Terminal may access Documents, allow access for this workshop folder.

## 7. Start JupyterLab

```console
uv run jupyter lab
```

Terminal prints messages and opens JupyterLab in your web browser. Leave Terminal running. In the browser, double-click `notebooks`, then `00_check_setup.ipynb`. At the upper right, select **Python (napari workshop)**. Run one code cell at a time with **Shift+Enter** and compare each result with the notebook’s explanation. Stop when the practice sphere appears: inspect and rotate it before running the cell that closes the viewer. Do not use **Run All Cells** for this interactive check.

Napari opens in a separate desktop window; use **Command+Tab** or check behind the browser if it is hidden.

To finish, save the notebook with **File → Save Notebook**, close napari, and choose **File → Shut Down** in JupyterLab. Close Terminal after the command stops. On another day, open Terminal, return to the workshop folder, and run `uv run jupyter lab` again.

> Check both the viewer and movie export before class. If either fails, send the instructor your macOS version, chip, and the complete error message. See the [validation record](../instructor/validation-report.md) for tests completed so far and remaining Mac checks.
