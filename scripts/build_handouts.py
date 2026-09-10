# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#   "sphinx>=8,<9",
#   "myst-nb>=1.2,<2",
#   "sphinx-book-theme>=1.1,<2",
# ]
# ///
"""Build online HTML handouts and a portable offline ZIP."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = PROJECT_ROOT / "_build" / "html"
DIST_DIR = PROJECT_ROOT / "dist"
ZIP_PATH = DIST_DIR / "napari-workshop-handouts.zip"


def _safe_remove_tree(path: Path) -> None:
    """Remove one known build directory without accepting an arbitrary target."""
    resolved = path.resolve()
    expected = (PROJECT_ROOT / "_build" / "html").resolve()
    if resolved != expected:
        raise RuntimeError(f"Refusing to remove unexpected path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def build_html() -> None:
    """Run Sphinx with the repository root as its source directory."""
    _safe_remove_tree(HTML_DIR)
    HTML_DIR.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "--keep-going",
            "-c",
            str(PROJECT_ROOT / "docs"),
            "-b",
            "html",
            str(PROJECT_ROOT),
            str(HTML_DIR),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


def write_root_redirect() -> None:
    """Give GitHub Pages and the offline ZIP a root-level entry point."""
    (HTML_DIR / "index.html").write_text(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=docs/index.html">
  <title>Rendering biological data with napari</title>
</head>
<body>
  <p><a href="docs/index.html">Open the napari workshop handouts</a>.</p>
</body>
</html>
""",
        encoding="utf-8",
    )


def build_offline_zip() -> None:
    """Package the exact HTML tree with index.html at a predictable top level."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    ZIP_PATH.unlink(missing_ok=True)
    archive_root = Path("napari-workshop-handouts")
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted(HTML_DIR.rglob("*")):
            if source.is_file():
                relative = source.relative_to(HTML_DIR)
                archive.write(source, archive_root / relative)


def main() -> None:
    build_html()
    write_root_redirect()
    build_offline_zip()
    print(f"HTML: {HTML_DIR}")
    print(f"Offline ZIP: {ZIP_PATH}")


if __name__ == "__main__":
    main()
