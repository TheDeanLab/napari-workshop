# Instructor teaching guide

## Course promise and boundary

In 180 minutes, learners use JupyterLab and napari to load a prepared four-dimensional microscopy dataset, interpret display choices, overlay precomputed detections and tracks, and export a view. They should leave able to explain what each layer represents and name important limitations.

The course does **not** compute new detections or tracks. Do not turn a rendering question into an algorithm lesson, and do not describe the supplied candidates or associations as validated biological truth. The original layer names are DNA and mitochondria; detailed particle identity remains unconfirmed. Voxel spacing and acquisition timing also remain unconfirmed, so teach source voxels and frame indices only. Do not show a physical scale bar, seconds, speeds, or physical distances.

The teaching package retains all 30 time frames and reduces each spatial dimension by factor 4. State early that this improves laptop usability while losing fine detail. The complete source image arrays are about 7.53 GiB before overhead; the full source download is about 8.1 GB.

Reference material: {download}`time-series MP4 <../reference/time-series.mp4>` and [2D view](../reference/viewer-2d-interface.png).

## Before learners arrive

At least one week before class:

1. Send the OS-specific setup page and ask learners to complete `00_check_setup.ipynb`.
2. Ask them to report OS version, processor, RAM, and whether a tiny GUI and movie check passed.
3. Hold a short installation clinic for managed computers.
4. Put verified copies of the workshop ZIP, `teaching.zip`, static handouts, representative PNGs, and a reference MP4 on two local drives.
5. Rehearse with the exact tagged release and a clean extracted folder, including a path with spaces.
6. Check the projector at normal room distance. Enlarge notebook and napari text as needed.
7. Confirm that the teaching package, tables, and source attribution match the pinned manifest.
8. Prepare pairs so every learner can continue if one computer has graphics trouble.

Do not claim Windows, Apple Silicon, or Intel macOS support until the relevant pilot is recorded. A documentation build checks links and structure; it does not test Qt, 3D interaction, memory, or movie encoding.

## Room setup and roles

Use one lead instructor and, if possible, one helper. The lead keeps the biological question and shared pace; the helper handles installation, wrong-folder, and wrong-kernel problems without stopping the room. Ask learners to keep browser, napari, and terminal visible as three distinct tools.

Display a final example at the start. Use a repeated rhythm: **predict → run a short cell → manipulate napari → explain the result**. When introducing syntax, say what each line changes before running it. Avoid live coding beyond edits already marked in the notebook.

## Exact 180-minute schedule

| Time | Activity | Check for understanding | Recovery/omit decision |
|---|---|---|---|
| 0–10 | Show the final view/movie; name browser, kernel, and napari window | Learners identify which window runs code and which displays data | Use a local reference movie if playback fails |
| 10–20 | Setup and data check; verify kernel and `sys.executable` | Path contains current workshop folder and `.venv`; tiny viewer opens | Stop downloads at minute 5; distribute local copy or pair |
| 20–40 | Load first grayscale image; explain array, axes, shape, layer | Learner labels `t,z,y,x` and finds the layer list | Use supplied 2D PNG if viewer fails |
| 40–65 | Add both channels; contrast, gamma, colormaps, opacity, additive blending; PNG export | Learner explains why display changes do not alter TIFF values | Keep screenshot; omit extra styling variations |
| 65–90 | Navigate z and t; compare slice, projection, and 3D; rotate/reset | Learner names information lost by projection | Use slice/projection and paired 3D route |
| 90–100 | Break | Helper resolves only bounded setup issues | Restart kernels/viewers as needed |
| 100–120 | Inspect five detection rows; add and style points | Learner matches one `t,z,y,x` row to one displayed marker | Instructor demonstrates table-to-point match |
| 120–140 | Add precomputed tracks; inspect ID, tail, width, and color | Learner explains association uncertainty and tail meaning | Use static track screenshot if interaction fails |
| 140–155 | Fixed-camera time sequence, then camera keyframes | Learner distinguishes sample time from camera motion | Omit camera keyframes first if behind |
| 155–165 | Export/check MP4 and retain PNG fallback | Learner distinguishes acquisition frame from playback fps | Use PNG plus reference MP4 if encoding fails |
| 165–177 | Independent mini-challenge | Learner produces an artifact and explains three choices and one limit | Pair or use prepared 2D data |
| 177–180 | Exit ticket and shutdown | Learner states image/detection/track distinction | Collect written answer after class if needed |

The ten-minute break belongs inside the 180 minutes. Give a visible warning at minutes 80, 135, and 155 so optional material cannot consume the final challenge.

## Demonstration notes and answers

### Setup and axes

Ask learners to run `import sys; print(sys.executable)`. The correct answer contains the current extracted workshop folder and `.venv`; seeing the display name alone is insufficient after a folder move. Thirty timepoints use indices 0–29 because Python and napari index from zero. `t` selects an acquisition frame; `z` selects depth within that frame.

### Display controls

Expected answer: contrast limits, gamma, colormap, opacity, and blending alter the mapping from values to the screen. They do not edit the TIFF intensities. Additive blending can make overlap visible but can also saturate bright regions. Toggling channels separately reveals whether a mixed color arises from both signals or from display choices.

### Slice, projection, and 3D

A slice shows one depth plane. A maximum-intensity projection selects the brightest value along depth and discards where that value occurred along `z`; separated structures may appear superimposed. A 3D rendering uses the acquired volume but is still a view controlled by camera, transfer function, contrast, and graphics sampling. It does not create new observations.

### Detections

The location columns are `t,z,y,x`. `amp` and `int` are supplied numeric measurements, but without validated definitions and biological controls they do not prove particle identity. Image and table transforms must match or a correct source coordinate will be rendered at the wrong feature.

### Tracks

The first column identifies a track; the remaining columns locate it at a frame. A longer tail shows more of the track’s recent time window, not more particles. A smooth path can still be wrong because nearby candidates may have been linked incorrectly, detections may be missing, or one biological object may be confused with another. Visual plausibility is useful QC, not validation.

### Export

Saving a notebook preserves its code, narrative, and stored outputs. Exporting writes a separate PNG or MP4. Playback fps determines how rapidly movie frames are shown; it is not the acquisition interval. Camera interpolation changes the viewpoint between keyframes and is not biological motion. A successful export should be reopened and checked for dimensions, frame count, first/last view, and intended layer/time change.

### Optional large-data comparison

Factor 1 preserves most source detail and requires the largest arrays; factors 2, 4, and 8 trade detail for lower display workload. A factor-4 package cannot produce factors 1 or 2. Lazy loading delays reads and may reduce RAM use. It does not reduce prior download size, guarantee instant scrubbing, or eliminate GPU memory for displayed data.

## Mini-challenge rubric

Give one point for each item:

1. The view and visible layers support a stated question.
2. Contrast/color/blending choices are explained without claiming they changed source values.
3. Points or tracks are interpreted as supplied candidates/associations.
4. A PNG or MP4 is written to a new output folder and located.
5. One specific limitation is stated: factor-4 detail loss, projection depth loss, unconfirmed calibration/timing, or tracking uncertainty.

Three of five demonstrates the core outcome. Do not award the interpretation points for simply producing an attractive image.

## Common misconceptions to address aloud

- “Jupyter is napari.” JupyterLab is the browser interface; napari is a separate local desktop viewer; the kernel runs Python.
- “Bright means more molecule.” Display brightness depends on several settings and the acquisition response; it is not automatically a concentration.
- “Overlap proves interaction.” Projection and additive blending can create apparent overlap.
- “A point is a particle.” It is a supplied candidate at a coordinate.
- “A line proves continuous identity.” It is an inferred association across discrete frames.
- “Tail length is particle count.” It is a frame window.
- “24 fps means the microscope acquired at 24 fps.” It is playback speed only.
- “Lazy means everything is small.” Requested chunks and GPU textures still consume resources.

## Recovery routes

### Five-minute download rule

Start the clock when an in-class teaching-package download begins. At five minutes, stop waiting and switch to a local copy or pair. Do not begin the 8.1 GB source download during the core lesson.

### 2D route

Set `USE_3D = False` in the main notebook’s first code cell before running the lesson (restart the kernel first if 3D already failed). Both 3D transitions and camera-only animation are skipped; the projection and its overlays remain available through PNG and acquired-time export. Keep the same sequence: load channels, adjust display, overlay 2D points/tracks, export PNG, interpret limitations. Explicitly state that a projection discards depth. If movie export works, a fixed-camera 2D time sequence can still meet most export objectives.

### Paired route

The learner with the functioning machine controls napari only after the partner predicts the action. Switch control at each checkpoint. Both learners record the interpretation and limitation. This preserves active participation; observing silently is an instructor demonstration rather than independent proficiency.

### Static route

When Qt fails entirely, use the offline HTML, annotated PNGs, printed quick reference, and reference MP4. Ask the learner to identify axes, layers, display choices, and interpretation limits. Record the missing hands-on outcome and arrange a later workstation session.

### When time is short

Omit, in order: additional styling variants, camera-keyframe animation, then optional large-data comparison. Preserve the image-versus-detection-versus-track distinction, one export, the mini-challenge, and exit ticket.

## Exit ticket prompts and expected elements

1. **What differs among an intensity, a detection, and a track?** An intensity is a stored voxel value; a detection is a candidate position at one frame; a track is an inferred association across frames.
2. **What changed when you adjusted contrast?** The display mapping changed; the TIFF values did not.
3. **Name one conclusion these materials cannot support yet.** Examples: physical distance or speed, elapsed seconds, particle identity, or proof that an association is correct.

## After class

Collect setup failures separately from scientific questions. Preserve exported artifacts and the environment/version record. Record which OS/processor combinations actually passed load, 3D interaction, and MP4 export; these are separate checks. Revise claims only from observed evidence. Point learners to `03_optional_large_data.ipynb` and `use-your-own-data.md` for take-home work, with the same calibration and alignment safeguards.
