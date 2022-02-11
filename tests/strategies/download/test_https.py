"""Tests the download strategy for 'https://' and 'http://'."""
# pylint: disable=invalid-name
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from requests_mock import Mocker


@pytest.mark.parametrize(
    "scheme,mediaType,filename",
    [
        ("http", "image/jpeg", "sample_1280_853.jpeg"),
        ("https", "image/jpeg", "sample_1280_853.jpeg"),
        ("http", "application/json", "sample2.json"),
        ("https", "application/json", "sample2.json"),
    ],
    ids=["http-binary", "https-binary", "http-text", "https-text"],
)
def test_https(
    scheme: str,
    mediaType: str,
    filename: str,
    static_files: "Path",
    requests_mock: "Mocker",
) -> None:
    """Test `https.py` download strategy by mocking downloads and comparing data mock
    downloaded from local copies with data obtained from simply opening them
    directly."""
    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.plugins.factories import create_strategy

    sample_file = static_files / filename
    assert sample_file.exists(), f"Test file not found at {sample_file} !"

    config = ResourceConfig(
        downloadUrl=f"{scheme}://this.is.not/real.url",
        mediaType=mediaType,
    )

    # Mock requests call in the download strategy
    requests_mock.get(config.downloadUrl, content=sample_file.read_bytes())

    download = create_strategy("download", config)
    datacache_key = download.get(config.downloadUrl).get("key", "")

    datacache = DataCache()
    mock_data = datacache.get(datacache_key)
    del datacache[datacache_key]
    assert mock_data == sample_file.read_bytes()
