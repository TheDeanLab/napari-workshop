# Rendering biological data with napari

Welcome to the online handouts for **napari Workshop Datasets: Deciphering the Living Cell through Microscopy and Computation**, November 16–17, 2026.

This three-hour workshop is written for biologists with little or no programming experience. Start with your operating system setup page before class. In the main notebook, you will load images, adjust how they look, add detections and tracks, and save a PNG or short movie.

[Download the course files](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.3/napari-workshop-v0.1.3.zip) · [Download offline HTML handouts](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.3/napari-workshop-handouts.zip)

Before typing commands, here are the tools you will use:

- **Python environment:** the workshop’s own Python and installed packages, stored in `.venv` so they stay together.
- **Terminal / PowerShell:** the command window where you install packages and start JupyterLab.
- **JupyterLab:** the application that opens a notebook in your browser. A notebook contains explanations and code cells.
- **Kernel:** the running Python process that executes those cells and remembers their variables. Select **Python (napari workshop)**. Restarting it clears those variables.
- **Napari:** the separate desktop window where you view and manipulate images and layers.

Keep the terminal running while you use JupyterLab and napari. More terms are in the [glossary](../handouts/glossary.md).

To open napari, run the notebooks on your computer using the setup instructions below.

![Napari interface displaying a 3D view with image, particle, and track layers](../reference/viewer-interface.png)

This view shows frame 10 of the teaching data. A [matching 2D projection](../reference/viewer-2d-interface.png) shows the same frame with depth flattened.

{download}`Download the reference time-series MP4 <../reference/time-series.mp4>` (30 acquisition frames, displayed at 10 playback frames per second; source data CC BY 4.0).

```{admonition} About the data
The points and tracks have already been computed. We will explore them alongside the images. Positions are in source voxels and time is shown as a frame number; converting to micrometres and seconds will require confirmation of the voxel size and acquisition interval.
```

```{toctree}
:maxdepth: 2
:caption: Begin

../README
../setup/windows
../setup/macos
../setup/download-data
../setup/troubleshooting
```

```{toctree}
:maxdepth: 2
:caption: Workshop notebooks

../notebooks/00_check_setup
../notebooks/01_rendering_workshop
../notebooks/02_optional_animation
../notebooks/03_optional_large_data
```

Notebook source files:

- {download}`Download the setup notebook <../notebooks/00_check_setup.ipynb>`
- {download}`Download the main workshop notebook <../notebooks/01_rendering_workshop.ipynb>`
- {download}`Download the optional animation notebook <../notebooks/02_optional_animation.ipynb>`
- {download}`Download the optional large-data notebook <../notebooks/03_optional_large_data.ipynb>`

```{toctree}
:maxdepth: 2
:caption: Student handouts

../handouts/quick-reference
../handouts/glossary
../handouts/exercises
../handouts/use-your-own-data
```

```{toctree}
:maxdepth: 2
:caption: Instructor materials

../instructor/teaching-guide
../instructor/slide-outline
../instructor/solutions
../instructor/validation-report
```

The [teaching dataset](https://doi.org/10.5281/zenodo.22696913) and [original source dataset](https://doi.org/10.5281/zenodo.22694247) have separate Zenodo records, both under CC BY 4.0. The teaching package keeps all 30 frames with roughly one-quarter as many samples along each spatial axis. It is small enough to use on a laptop, though some fine detail is lost. Follow [Download the data](../setup/download-data.md) to get your copy.
