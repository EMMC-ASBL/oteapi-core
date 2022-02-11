"""Tests the download strategy for 'file://'."""
# pylint: disable=invalid-name
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    "filename,mediaType",
    [("sample_1280_853.jpeg", "image/jpeg"), ("sample2.json", "application/json")],
    ids=["binary", "text"],
)
def test_file(filename: str, mediaType: str, static_files: "Path") -> None:
    """Test `file` download strategy on binary and text files.

    Test files are taken from filesamples.com.
    """
    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.file import FileStrategy

    sample_file = static_files / filename
    assert sample_file.exists(), f"Test file not found at {sample_file} !"

    # Test binary file download
    config = ResourceConfig(
        downloadUrl=sample_file.as_uri(),
        mediaType=mediaType,
    )
    output = FileStrategy(config).get()
    content: bytes = DataCache().get(output["key"])

    if mediaType.startswith("image"):
        # binary
        assert content == sample_file.read_bytes()
    else:
        # text
        assert content.decode(encoding="utf8") == sample_file.read_text(encoding="utf8")
