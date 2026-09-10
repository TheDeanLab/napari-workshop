"""Sphinx configuration for the napari workshop handouts."""

from __future__ import annotations

project = "Rendering biological data with napari"
author = "The Dean Lab"
copyright = f"2026, {author}"

extensions = ["myst_nb"]
source_suffix = {".md": "myst-nb", ".ipynb": "myst-nb"}
master_doc = "docs/index"

# Course notebooks open a local Qt viewer and require downloaded microscopy data.
# Documentation builds therefore render stored content without executing cells.
nb_execution_mode = "off"
myst_enable_extensions = ["colon_fence", "deflist"]

exclude_patterns = [
    ".git/**",
    ".github/**",
    ".pytest_cache/**",
    ".venv/**",
    "_build/**",
    "dist/**",
    "data/**",
    "outputs/**",
    "scripts/**",
    "src/**",
    "tests/**",
    "WORKSHOP_PLAN.md",
]

html_theme = "sphinx_book_theme"
html_title = project
html_baseurl = "https://thedeanlab.github.io/napari-workshop/"
html_theme_options = {
    "repository_url": "https://github.com/TheDeanLab/napari-workshop",
    "use_repository_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs",
}
html_static_path: list[str] = []
