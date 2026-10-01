"""Конфигурация Sphinx."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# autodoc импортирует пакеты из исходников, без установки
sys.path[:0] = [
    str(ROOT / "packages" / "core" / "src"),
    str(ROOT / "app" / "api" / "src"),
]

project = "Order calculator"
author = "artixdev-spec"
release = "0.1.0"
language = "ru"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinxcontrib.mermaid",
]

myst_fence_as_directive = ["mermaid"]
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build", "diagrams/*.mmd"]

autodoc_member_order = "bysource"
autodoc_typehints = "description"

html_theme = "alabaster"
