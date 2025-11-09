"""Pytest configuration for the test suite."""

from __future__ import annotations

import sys
from pathlib import Path


def _configure_path() -> None:
    """Ensure the source directory is importable when tests run locally."""
    src_dir = Path(__file__).resolve().parent.parent / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))


_configure_path()
