# Windows setup

Complete this setup before class if you can. You need an internet connection, permission to install software for your Windows account, and about 10 GB of free space. These directions use **PowerShell**, the command window built into Windows.

Before typing commands, here are the tools you will use:

- **Python environment:** the workshop’s own Python and installed packages, stored in `.venv` so they stay together.
- **Terminal / PowerShell:** the command window where you install packages and start JupyterLab.
- **JupyterLab:** the application that opens a notebook in your browser. A notebook contains explanations and code cells.
- **Kernel:** the running Python process that executes those cells and remembers their variables. Select **Python (napari workshop)**. Restarting it clears those variables.
- **Napari:** the separate desktop window where you view and manipulate images and layers.

Keep the terminal running while you use JupyterLab and napari. More terms are in the [glossary](../handouts/glossary.md).

## 1. Open PowerShell

Open the **Start** menu, type `PowerShell`, and choose **Windows PowerShell** or **PowerShell**. A window with a prompt such as `PS C:\Users\YourName>` appears. The prompt shows the folder where a command will run. Type only the commands shown after the prompt, then press **Enter**.

Do not choose “Run as administrator.” If your organization blocks PowerShell scripts or software installation, stop and ask its support staff or the workshop instructor for the prepared classroom computer route.

## 2. Install uv

`uv` installs the correct Python version and all packages recorded for this workshop. Copy this command from the [official uv installation page](https://docs.astral.sh/uv/getting-started/installation/), paste it into PowerShell, and press **Enter**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

The command temporarily permits the downloaded installer to run. `irm` retrieves the official installer and `iex` runs it. If you are not permitted to run downloaded scripts, do not weaken a managed-machine policy; use the instructor’s fallback.

Close PowerShell, reopen it, and verify the installation:

```powershell
uv --version
```

Success looks like `uv 0.x.y` (the numbers may differ). If PowerShell says that `uv` is not recognized, close every PowerShell window and try once more, then see [troubleshooting](troubleshooting.md).

## 3. Download and extract the workshop folder

Download the **course files**, [`napari-workshop-v0.1.3.zip`](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.3/napari-workshop-v0.1.3.zip). This release includes the revised documentation and the November setup and rendering fixes. Extract it into a fresh folder rather than mixing it with an older course copy.

| ZIP file | Purpose |
|---|---|
| `napari-workshop-v0.1.3.zip` | Required: notebooks, scripts, and Python environment files. Extract this as your workshop folder. |
| `napari-workshop-handouts.zip` | Optional: offline reading in a browser. It cannot replace the course files. |
| `teaching.zip` | Microscopy data, downloaded separately in the data step below. |

In File Explorer, open **Downloads**, right-click the ZIP, choose **Extract All…**, and select a short location such as `C:\Users\YourName\Documents`. Click **Extract**.

Open the extracted folder. It must directly contain `README.md`, `pyproject.toml`, `uv.lock`, `notebooks`, and `scripts`. GitHub ZIPs often add a suffix, so the actual folder may be named `napari-workshop-main`; that is fine.

## 4. Move PowerShell into the folder

In File Explorer, click the folder’s address bar, type `powershell`, and press **Enter**. A new PowerShell window opens in that folder. Verify the contents:

```powershell
Get-ChildItem
```

You should see `pyproject.toml`, `uv.lock`, and the `notebooks` and `scripts` folders. If you do not, you may be one folder too high or inside an extra nested ZIP folder.

You can also change folders explicitly. Quotation marks keep paths containing spaces together:

```powershell
cd "$HOME\Documents\napari-workshop-main"
```

## 5. Create the workshop environment

Run:

```powershell
uv sync --locked
```

`uv sync` creates a private `.venv` environment inside this workshop folder and installs its packages. `--locked` requires the tested dependency record in `uv.lock` instead of silently choosing newer versions. uv may download Python 3.12 first. The initial run can take several minutes; later runs are usually faster.

Success ends without red error text and leaves a hidden `.venv` folder. You do not need to activate it. Keep `.venv` in the extracted workshop folder.

Register the environment as a Jupyter kernel:

```powershell
uv run python -m ipykernel install --user --name napari-workshop --display-name "Python (napari workshop)"
```

This runs Python from `.venv` and creates the human-readable kernel choice **Python (napari workshop)**. Success includes a message beginning `Installed kernelspec`.

## 6. Download the teaching data

Follow [Download the data](download-data.md). The recommended command is:

```powershell
uv run scripts/download_data.py --dataset teaching
```

## 7. Check the setup

First run the command-line checks:

```powershell
uv run python scripts/check_setup.py
```

Success lists a Python executable inside this workshop’s `.venv`, napari 0.6.6 and other package versions, available RAM, and `Checks complete`. The exact folder and RAM number vary by computer.

Then test a tiny napari window:

```powershell
uv run python scripts/check_setup.py --gui
```

A separate napari window should appear. Close it after the test. Add `--movie` only when the instructor asks you to test movie export.

## 8. Start JupyterLab

```powershell
uv run jupyter lab
```

PowerShell prints messages and opens JupyterLab in your web browser. Leave PowerShell running. In the browser, double-click `notebooks`, then `00_check_setup.ipynb`. At the upper right, select **Python (napari workshop)**. Run one code cell at a time with **Shift+Enter** and compare each result with the explanation in the notebook. Stop when the practice sphere appears: inspect and rotate it before running the cell that closes the viewer. Do not use **Run All Cells** for this interactive check.

The notebook runs in the browser, while napari opens as a separate desktop window. Look behind the browser or use **Alt+Tab** if the viewer is hidden.

To finish, save the notebook with **File → Save Notebook**, close the napari window, and in JupyterLab choose **File → Shut Down**. Close PowerShell after the command has stopped. To return on another day, open PowerShell in the workshop folder and run `uv run jupyter lab` again.

> If a step fails, send the instructor your Windows version, processor type, and the complete error message. The [validation record](../instructor/validation-report.md) lists the Windows checks that still need to be completed.
