# Glossary

**Acquisition frame**

One recorded observation in a time series. This workshop labels frames `0` through `29`. A frame index is not elapsed time unless the acquisition interval is known.

**Additive blending**

A display mode that adds light from image layers, helping two channels appear together. Bright overlap can saturate, so inspect each channel separately too.

**Array**

A rectangular collection of numbers. A microscopy image is represented as an array whose axes may describe time, depth, rows, and columns.

**Channel**

An image series acquired for a particular signal. The two channels in this workshop are named DNA and mitochondria.

**Colormap**

A rule that maps numerical intensity to displayed color. Changing it does not alter stored intensity values.

**Contrast limits**

The low and high intensity values mapped to the dark and bright ends of a layer’s display. Values outside the limits may appear clipped.

**Detection**

The location of a possible particle in one frame. Detections can include mistakes, so compare them with the image.

**Downsampling factor**

How much the original spatial grid is reduced. Factor 4 reduces the number of samples along each spatial axis to roughly one-quarter. It reduces workload but loses fine detail. It does not change the 30-frame time axis.

**Dtype**

The number format stored by an array. `uint16` stores non-negative integers from 0 through 65,535.

**Environment (`.venv`)**

The folder containing this workshop’s Python and packages. `uv sync --locked` creates it. It stays inside the workshop folder and does not need manual activation.

**Gamma**

A nonlinear display adjustment that redistributes apparent brightness between the contrast limits. It changes appearance, not the source values.

**Intensity**

A numeric image value measured at a voxel. Brightness on screen also depends on contrast, gamma, colormap, opacity, and blending.

**Jupyter kernel**

The Python process that runs notebook cells. Choose **Python (napari workshop)** so the notebook uses the workshop environment.

**JupyterLab**

The application that opens notebooks in your browser. A notebook combines explanations and runnable code cells. JupyterLab sends code to the selected kernel; the browser itself does not execute the Python code.

**Layer**

One image, points table, tracks table, or other object in the napari viewer. Each layer has its own visibility and display controls.

**Lazy loading**

Reading pieces of an array as they are needed. This can reduce RAM use, though loading each new piece takes time and the displayed data still use graphics memory. The initial download is the same size.

**Maximum-intensity projection (MIP)**

A 2D image containing the brightest voxel found along a chosen axis, often depth. It shows bright structures together but discards their positions along the projected axis.

**Napari**

An interactive desktop viewer for multidimensional images and related data. It opens separately from the JupyterLab browser.

**Notebook cell**

A block of Markdown explanation or Python code. Run code cells from top to bottom with **Shift+Enter**.

**Opacity**

How transparent a layer appears. Reducing opacity can reveal another layer beneath it.

**Playback fps**

Frames shown per second in an exported movie. It controls viewing speed and does not establish acquisition timing.

**Point**

A marker displayed at a coordinate. In this workshop points visualize precomputed detection-table rows.

**Projection**

A lower-dimensional summary of an array. Always state which axis and operation were used because a projection loses information.

**Scale**

The conversion between array steps and physical units. We still need to confirm the voxel size for this dataset, so positions are shown in source voxels.

**Slice**

One plane selected from a volume. Unlike a projection, it does not combine all depth planes.

**Source voxel**

One element of the original three-dimensional image grid. Tables retain source-voxel coordinates even when the prepared image array is spatially reduced; the course loader aligns them.

**Track**

An inferred association of positions across frames, identified by `id`. Tracking software links detections into a path, sometimes making incorrect or ambiguous connections.

**Track tail**

The recent portion of a track displayed behind its current point. Tail length describes a window in frame indices, not a particle count.

**Voxel**

A volume element: the 3D counterpart of a pixel. Its physical size must come from verified calibration.

**Zero-based indexing**

Counting that starts at zero. Thirty frames therefore use indices `0` through `29`.
