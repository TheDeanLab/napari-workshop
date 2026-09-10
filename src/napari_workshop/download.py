"""Verified downloads; only standard-library dependencies are required."""

import hashlib
import json
import shutil
import stat
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath


def checksum(path, algorithm="md5"):
    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verified(path, spec):
    algorithm, expected = spec["checksum"].split(":", 1)
    path = Path(path)
    return (
        path.is_file()
        and path.stat().st_size == spec["size"]
        and checksum(path, algorithm) == expected
    )


def download_file(spec, destination, attempts=3, local_file=None):
    """Resume a partial transfer where supported; publish only verified bytes."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    name = spec["name"]
    if Path(name).name != name or name in (".", "..") or "\\" in name:
        raise ValueError("Unsafe download filename")
    target = destination / name
    if target.exists():
        if verified(target, spec):
            print(f"Verified existing {name}", flush=True)
            return target
        raise ValueError(
            f"Existing {target} has the wrong size/checksum. Move it aside and retry."
        )
    partial = target.with_name(name + ".part")
    if local_file is not None:
        if not verified(local_file, spec):
            raise ValueError(f"Local source checksum differs from Zenodo: {local_file}")
        shutil.copyfile(local_file, partial)
        if not verified(partial, spec):
            raise ValueError(f"Copied file checksum mismatch: {name}")
        partial.replace(target)
        return target
    for attempt in range(attempts):
        try:
            if partial.exists() and verified(partial, spec):
                partial.replace(target)
                return target
            offset = partial.stat().st_size if partial.exists() else 0
            if offset >= spec["size"]:
                partial.unlink()
                offset = 0
            headers = {
                "User-Agent": "TheDeanLab-napari-workshop/0.1",
                "Accept-Encoding": "identity",
            }
            if offset:
                headers["Range"] = f"bytes={offset}-"
            request = urllib.request.Request(spec["url"], headers=headers)
            with urllib.request.urlopen(request, timeout=60) as response:
                resumed = response.status == 206
                if resumed and not response.headers.get("Content-Range", "").startswith(
                    f"bytes {offset}-"
                ):
                    raise ValueError("Server returned an unexpected byte range")
                if not resumed:
                    offset = 0
                mode = "ab" if resumed else "wb"
                last_report = offset
                with partial.open(mode) as stream:
                    while block := response.read(1024 * 1024):
                        offset += len(block)
                        if offset > spec["size"]:
                            raise ValueError("Download exceeded the published file size")
                        stream.write(block)
                        if offset - last_report >= 16 * 1024 * 1024:
                            print(f"{name}: {offset / spec['size']:.0%}", flush=True)
                            last_report = offset
            if not verified(partial, spec):
                partial.unlink(missing_ok=True)
                raise ValueError(f"Checksum/size verification failed: {name}")
            partial.replace(target)
            print(f"Downloaded and verified {name}", flush=True)
            return target
        except (OSError, ValueError, urllib.error.URLError) as error:
            if attempt + 1 == attempts:
                raise RuntimeError(
                    f"Download failed: {name}: {error}. Check your connection and retry."
                ) from error
            print(f"Retrying {name}: {error}", flush=True)
            time.sleep(attempt + 1)
    raise RuntimeError("No download attempts requested")


def extract_teaching(archive, destination):
    """Extract into a fresh directory after checking paths and file checksums."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            path = PurePosixPath(info.filename)
            if (
                path.is_absolute()
                or ".." in path.parts
                or "\\" in info.filename
                or ":" in info.filename
                or stat.S_ISLNK(info.external_attr >> 16)
            ):
                raise ValueError(f"Unsafe ZIP member: {info.filename}")
        metadata = json.loads(z.read("metadata.json"))
        specs = metadata["files"]
        if destination.exists():
            existing = json.loads((destination / "metadata.json").read_text())
            if existing == metadata and all(verified(destination / f["name"], f) for f in specs):
                print(f"Verified extracted dataset: {destination}")
                return destination
            raise ValueError(
                f"Existing dataset differs: {destination}. Choose a new folder or move it aside."
            )
        with tempfile.TemporaryDirectory(
            dir=destination.parent, prefix="teaching-extract-"
        ) as temp:
            extracted = Path(temp) / "dataset"
            extracted.mkdir()
            z.extractall(extracted)
            if not all(verified(extracted / f["name"], f) for f in specs):
                raise ValueError("Extracted dataset checksum mismatch")
            extracted.rename(destination)
    return destination
