# Exercises

Run these exercises in `notebooks/01_rendering_workshop.ipynb` unless your instructor gives another route. Save your notebook before each challenge. The supplied points and tracks are precomputed; do not run a detector or tracker.

## 1. Find the axes

1. Run the loading cells in order.
2. Write down the shape of one image array.
3. Label the axes `t,z,y,x`.
4. Move only the `t` slider, then return it to frame 0.
5. Move only the `z` slider.

**Explain:** Which slider changes recorded time and which moves within one 3D volume? Why does a 30-frame series end at index 29?

**Checkpoint:** You can return to the same `t` and `z` location and point to both slider labels.

## 2. Display choices are interpretations

1. Select the DNA image layer and hide the mitochondria layer.
2. Adjust contrast limits until both bright and dim structure are visible.
3. Change gamma and then restore it to the notebook value.
4. Show the mitochondria layer, choose a distinct colormap, and use additive blending.
5. Toggle each layer off and on before judging overlap.

**Predict first:** Will these controls change any numbers stored in the TIFF files?

**Explain:** Name two display choices that could make an apparent overlap look stronger or weaker. Why should you inspect channels separately?

**Checkpoint:** Save a screenshot to the new output path specified in the notebook and describe the choices in one sentence.

## 3. Slice, projection, and 3D view

1. Find one recognizable feature in a single z slice.
2. Compare it with the maximum-intensity projection.
3. If graphics permit, switch to 3D and rotate the volume; press **Home** to reset.

**Explain:** What depth information did the projection discard? Does the 3D rendering create measurements that were not acquired?

**Fallback:** If 3D is slow or blank, complete the comparison with the 2D slice and projection. Pair with a participant whose 3D viewer works for the rotation task, or observe the instructor demonstration. Record that you used the fallback.

## 4. Match a table row to a point

1. Display the first five rows of `detections.csv` in the notebook.
2. Choose one row and read its `t,z,y,x` values aloud or write them down.
3. Navigate the viewer to its frame and depth.
4. Toggle the points layer and identify the corresponding marker.
5. Change the marker size for visibility, then restore it.

**Explain:** Which columns locate the point? What do `amp` and `int` not tell you by themselves? Why must an image and table use matching coordinate transforms?

## 5. Follow one supplied track

1. Select one track ID that is present in several rows.
2. Move through its frames and follow the marker.
3. Change the displayed tail length.
4. Hide and show the tracks layer to compare it with the points and images.

**Explain:** Does a longer tail mean that more particles were detected? Give one reason an inferred association might be wrong even when it looks smooth.

## 6. Independent mini-challenge

Create one view that communicates a feature you find interesting:

1. Choose a frame and a slice, projection, or 3D view.
2. Style both image layers deliberately.
3. Show supplied detections or tracks only when they help the claim.
4. Export a PNG into a new folder under `outputs/`.
5. If movie export works, make a short MP4; otherwise submit the PNG.
6. Write three display/export decisions and one limitation.

Your limitation should be specific—for example, reduced spatial detail, unconfirmed calibration, projection depth loss, or uncertainty in a supplied track. Do not label frame index as seconds or add a physical scale bar.

## Optional: prepared versus source resolution

Use `notebooks/03_optional_large_data.ipynb` only after the core lesson.

1. Before running, predict which spatial factor will require more memory and preserve more detail.
2. Load one source timepoint at two supported factors from `1,2,4,8`.
3. Compare array shapes and estimated byte counts.
4. Verify that an image feature and table marker stay aligned.
5. Describe what lazy loading changed and what it did not change.

A factor-4 teaching package cannot provide factor-1 detail. Lazy loading may limit RAM use, but it does not reduce download size or guarantee lower graphics use for the displayed volume.

## Take-home reflection

In three or four sentences, distinguish a voxel intensity, a candidate detection, an inferred track, and a display setting. State which conclusions require acquisition metadata or biological validation beyond this workshop.
