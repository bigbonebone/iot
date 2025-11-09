"""Basic tests for the iot package."""

from iot import __version__


def test_version() -> None:
    """Ensure the package exposes its version."""
    assert isinstance(__version__, str)
    assert __version__ != ""
