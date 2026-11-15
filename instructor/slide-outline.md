# Slide outline

This outline supports the 180-minute lesson. Keep slides sparse and switch quickly to the notebook and viewer.

## Opening and orientation (0–20 minutes)

### 1. Deciphering the living cell through microscopy and computation

- Workshop dates: November 16–17, 2026
- Today: explore images, add detections and tracks, and make a movie
- Show the final PNG or short movie

Speaker note: detections and tracks have already been computed. No new detection or tracking runs today.

### 2. Three windows, three jobs

- Terminal/PowerShell starts tools
- JupyterLab browser shows explanations and code cells
- Kernel executes Python and remembers variables
- Environment (`.venv`) holds this workshop’s Python and packages
- Napari desktop window displays and manipulates layers

Demo: locate each window and show how to switch among them.

### 3. Setup checkpoint

- Correct folder contains `pyproject.toml`
- Kernel is **Python (napari workshop)**
- `sys.executable` contains current folder and `.venv`
- All teaching files pass verification
- Practice sphere is visible and rotates

Speaker note: stop classroom downloads after five minutes and distribute the local copy.

## Images and display (20–90 minutes)

### 4. An image is an array

- Axes: `t,z,y,x`
- Thirty frames: indices 0–29
- Values: unsigned 16-bit intensities

Prompt: which axis is acquisition frame, and which is depth?

### 5. Layers keep data and controls organized

- Source layer names: DNA and mitochondria
- Visibility, contrast, colormap, opacity, blending
- Display settings do not alter stored TIFF values

### 6. Predict before adjusting

- What becomes visible if the upper contrast limit falls?
- What can additive blending conceal?
- Why toggle channels separately?

Demo: make one useful adjustment and one misleading saturated view.

### 7. Slice, projection, and 3D rendering

- Slice: one depth plane
- Maximum-intensity projection: brightest value, depth location discarded
- 3D: an interactive rendering of acquired voxels, not new data

Prompt: find one feature and compare all available views.

### 8. Why we use a smaller dataset

- All 30 frames retained
- Spatial factor 4
- Lower network/RAM/rendering demands
- Fine detail lost and unrecoverable from the package

Speaker note: source images are about 7.53 GiB in memory before overhead.

## Supplied measurements (100–140 minutes)

### 9. A detection is a candidate at one frame

- Columns: `t,z,y,x,amp,int`
- Match one row to one marker
- Coordinates must use the same transform as images

Speaker note: numeric measurements and visual alignment do not prove identity.

### 10. A track is an inferred association

- Columns: `id,t,z,y,x`
- 2,058 supplied track IDs
- Tail length is a time window
- Smooth-looking paths can still be wrong

Prompt: how might two detections get linked incorrectly?

### 11. What we know about the data

| Supported description | Awaiting evidence |
|---|---|
| Layer names DNA/mitochondria | Detailed tracked-particle identity |
| Frame indices 0–29 | Elapsed seconds/acquisition interval |
| Source-voxel coordinates | Micrometres/physical scale bar |
| Supplied candidates and associations | Biological validation |

## Export and communication (140–165 minutes)

### 12. Two different kinds of animation

- Fixed camera across acquired frames: sample changes over frame index
- Camera keyframes at one time: viewpoint changes
- Combined animation: explain both explicitly

Speaker note: camera interpolation creates views, not observations.

### 13. Saving versus exporting

- Save notebook: code, prose, cell outputs
- Export PNG: one rendered view
- Export MP4: rendered frames at a playback fps
- Use a fresh output folder and reopen the result

### 14. Playback speed is not acquisition time

- Movie fps controls presentation speed
- Use seconds only after timestamps are verified
- Check first/last frame, dimensions, and intended layer/time changes

## Challenge and close (165–180 minutes)

### 15. Independent mini-challenge

- Choose a view and style layers deliberately
- Include points/tracks only when useful
- Export PNG or MP4
- Explain three decisions and one limitation

Show the 2D, paired, and static fallback routes on the same slide.

### 16. Exit ticket

- Distinguish intensity, detection, and track
- State what contrast changed
- Name one unsupported conclusion

### 17. Try your own data

- Optional animation and large-data notebooks
- Use-your-own-data checklist: axes, units, memory, coordinates, provenance
- Teaching dataset DOI: `10.5281/zenodo.22696913` (CC BY 4.0)
- Original dataset DOI: `10.5281/zenodo.22694247` (CC BY 4.0)

Speaker note: ask what learners would need to check before interpreting tracks from their own experiment.
