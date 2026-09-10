# Download the data

Download the 42.8 MB teaching ZIP before class. It keeps all 30 time frames while reducing each spatial dimension by a factor of four; the extracted image arrays contain about 122.5 MiB. That reduction lowers download, memory, and rendering demands, but it permanently removes fine spatial detail.

The teaching derivative comes from [napari Workshop Datasets: Deciphering the Living Cell through Microscopy and Computation (2026)](https://doi.org/10.5281/zenodo.22694247) and is licensed CC BY 4.0. The derivative is archived separately at [Zenodo DOI 10.5281/zenodo.22696913](https://doi.org/10.5281/zenodo.22696913). Zenodo is the default download source; GitHub retains an identical mirror.

## Recommended: verified command-line download

Open PowerShell on Windows or Terminal on macOS. Move into the extracted workshop folder—the folder containing `pyproject.toml`—and preview the download:

```console
uv run scripts/download_data.py --dataset teaching --dry-run
```

For this script command, `uv run` uses the script’s own declared and locked environment. It does not change your Jupyter kernel. The script selects the named `teaching` package, and `--dry-run` reports what would be downloaded without writing it. The archive is cached in `data/downloads` and then extracted into `data/teaching`. Check that the reported size is practical for your connection.

Start the download:

```console
uv run scripts/download_data.py --dataset teaching
```

The downloader verifies the archive against the checksum recorded in the project manifest before extraction. Rerunning the same command is safe: a previously verified package can be reused, including one downloaded earlier from GitHub. Its bytes and checksum have not changed.

At an ideal sustained 10 Mbit/s the 42.8 MB transfer takes about 35 seconds, or about 3.5 seconds at 100 Mbit/s. Browser, server, Wi-Fi, verification, extraction, and a room full of shared connections add overhead, so these calculations are not a download-time promise.

Success produces this layout:

```text
data/teaching/
├── metadata.json
├── detections.csv
├── tracks.csv
├── ch0/
│   ├── frame_000000.tif
│   └── ...
└── ch1/
    ├── frame_000000.tif
    └── ...
```

Both channel folders should contain frames numbered from `frame_000000.tif` through `frame_000029.tif`. Do not rename individual frames.

## Browser download

If the command-line route is blocked, download [teaching.zip from Zenodo](https://zenodo.org/records/22696913/files/teaching.zip?download=1) in a browser. An identical [GitHub mirror](https://github.com/TheDeanLab/napari-workshop/releases/download/v0.1.0/teaching.zip) is available if Zenodo is unreachable.

1. Wait for the browser to finish downloading. A partial browser download is not usable.
2. Open the workshop folder, then open its `data` folder.
3. Extract the ZIP there. On Windows, right-click it and choose **Extract All…**. On macOS, double-click it.
4. The result must be `data/teaching/metadata.json`, not `data/teaching/teaching/metadata.json`. Move the inner folder up one level if extraction created an extra nested folder.
5. Keep the ZIP until the setup notebook confirms the data can be read.

The scripted route checks file identity automatically. With a browser download, use the setup notebook to check the extracted layout before class.

## Five-minute classroom limit

During class, stop a teaching-package download after five minutes if it is not complete. Tell the instructor and use the supplied USB/local copy, pair with a participant who has the data, or follow the static 2D route. Waiting longer consumes the lesson without teaching napari. This limit is a classroom decision, not a promised download time.

## Optional source data

The full source images are much larger. Preview every source request first:

```console
uv run scripts/download_data.py --dataset source --timepoints 5 --dry-run
```

The five-frame option downloads the first five raw volumes from **both** channels plus the tables, about 1.35 GB:

```console
uv run scripts/download_data.py --dataset source --timepoints 5
```

All 30 source frames require about 8.1 GB to download, before environment and output space:

```console
uv run scripts/download_data.py --dataset source --timepoints 30 --dry-run
uv run scripts/download_data.py --dataset source --timepoints 30
```

Use the 30-frame command only as optional take-home work on a suitable connection. The complete source image arrays alone occupy about 7.53 GiB in memory if loaded eagerly; the large-data notebook therefore demonstrates lazy loading. Lazy loading does not reduce the download, guarantee fast scrubbing, or remove GPU limits.

An instructor with verified original files can avoid another network transfer:

```console
uv run scripts/download_data.py --dataset source --timepoints 5 --local-source "/path/to/original files"
```

The quoted path may contain spaces. The script checks the local source before reuse.

## What is already computed

`detections.csv` contains supplied rows with columns `t,z,y,x,amp,int`. `tracks.csv` contains headerless rows in `id,t,z,y,x` order and represents 2,058 supplied tracks. The workshop reads and displays these tables. Downloading or opening them does **not** recompute detections or tracks, and no workshop step asks you to run detection or tracking.

The layer names **DNA** and **mitochondria** come from the source files. More specific particle identity, voxel calibration, and acquisition timing are awaiting confirmation. Treat `t` as a frame index and `z,y,x` as source-voxel coordinates; do not add seconds, micrometres, or a physical scale bar.
