# Rendering biological data with napari

This repository contains the materials for **napari Workshop Datasets: Deciphering the Living Cell through Microscopy and Computation**, a three-hour workshop for biologists on November 16–17, 2026.

You will use a Jupyter notebook to give instructions to Python and a separate napari window to explore a four-dimensional microscopy dataset. You will load two image layers named **DNA** and **mitochondria**, overlay supplied particle detections and tracks, adjust the display, and export a view. The detections and tracks are already computed. The workshop does not teach or run new detection or tracking calculations.

## Start here

Complete these steps before the workshop if possible:

1. Follow the instructions for [Windows](setup/windows.md) or [macOS](setup/macos.md).
2. [Download the teaching data](setup/download-data.md).
3. Open `notebooks/00_check_setup.ipynb` in JupyterLab and run its checks.
4. If something differs from the expected result, use [troubleshooting](setup/troubleshooting.md) or send the instructor the exact error text.

On the workshop day, start in the extracted `napari-workshop` folder and run:

```console
uv run jupyter lab
```

Open `notebooks/01_rendering_workshop.ipynb`. Choose **Kernel → Change Kernel… → Python (napari workshop)** if that name is not already shown at the upper right. Run cells from top to bottom. JupyterLab stays in the browser; napari opens in its own desktop window.

## Materials

- [Download and data guide](setup/download-data.md)
- [Troubleshooting](setup/troubleshooting.md)
- [One-page quick reference](handouts/quick-reference.md)
- [Glossary](handouts/glossary.md)
- [Exercises](handouts/exercises.md)
- [Use your own data](handouts/use-your-own-data.md)
- [Instructor teaching guide](instructor/teaching-guide.md)
- [Slide outline](instructor/slide-outline.md)

The optional notebooks add animation and a larger, lazily loaded source dataset. They are take-home material unless the instructor explicitly uses them.

## Reference view

![Napari showing DNA and mitochondria image layers with supplied particle and track overlays in a 3D view](reference/viewer-interface.png)

This is a real render of the prepared teaching data at frame index 10. The layer list and controls are on the left, the rendered volume is in the main canvas, and the frame slider is at the bottom. It was generated during Linux validation and is a visual checkpoint, not evidence that Windows or macOS has passed a platform test. A [2D projection reference](reference/viewer-2d-interface.png) is available for the fallback route.

## What the data represent

The source data have 30 frame indices per image channel. Each source image volume is `118 × 664 × 860` voxels with unsigned 16-bit intensity values. The complete two-channel image series occupies about 7.53 GiB before Python and graphics memory are counted. The 42.8 MB teaching ZIP keeps all 30 frames and reduces each spatial dimension by a factor of four; the extracted image arrays contain about 122.5 MiB. This makes it practical to display, but fine spatial detail has been lost and cannot be recovered from the prepared files.

Coordinates are expressed in source voxels and time is expressed as a zero-based frame index (`0` through `29`). Acquisition spacing and elapsed time have not yet been confirmed, so these materials do not claim micrometres, seconds, or a physical scale bar. The supplied `detections.csv` contains `t,z,y,x,amp,int`; `tracks.csv` contains `id,t,z,y,x` and 2,058 track IDs. A point is a supplied candidate detection. A track is a supplied inferred association of positions across frames; neither is direct proof of biological identity.

Dataset: [napari Workshop Datasets: Deciphering the Living Cell through Microscopy and Computation (2026)](https://doi.org/10.5281/zenodo.22694247), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The new workshop code is licensed under the BSD 3-Clause License.

## Requirements and status

Use Windows or macOS, about 10 GB of free disk space, and preferably 16 GB of RAM; 8 GB is the intended minimum for the prepared teaching package. A dedicated NVIDIA GPU is not required, but napari still needs working graphics/OpenGL support.

These instructions are being prepared for platform pilots. A successful documentation build does not establish that napari, 3D rendering, or movie export works on a particular student computer. Record the operating system, processor, and exact error if a setup check fails.

Read the [online walkthrough](https://thedeanlab.github.io/napari-workshop/) or download the [course ZIP](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.0/napari-workshop-v0.1.0.zip) and [offline HTML handouts](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.0/napari-workshop-handouts.zip). See the [validation record](instructor/validation-report.md) for tested behavior and remaining platform checks.
