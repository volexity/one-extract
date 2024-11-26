"""Libarary to extract data from OneNote files."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("one-extract")
except PackageNotFoundError:
    __version__ = "0.0.0-unknown"

from .one import (
    OneNoteExtractor,
    OneNoteExtractorError,
    OneNoteMetadataObject,
)

__all__ = [
    "OneNoteExtractor",
    "OneNoteExtractorError",
    "OneNoteMetadataObject",
]
