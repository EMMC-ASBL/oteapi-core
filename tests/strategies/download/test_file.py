"""Tests the download strategy for 'file://'."""
from pathlib import Path


def test_file():
    """Test `file` download strategy on 'sample_1280_853.jpeg' and
    'sample2.json', downloaded from filesamples.com.
    """
    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.file import FileStrategy

    path = Path(__file__).resolve().parents[1]
    url = path.as_uri().replace(":", "").replace("///", "://")

    # Test binary file download
    binary_config = ResourceConfig(
        downloadUrl=url + "/sample_1280_853.jpeg",
        mediaType="image/jpeg",
    )
    binary_output = FileStrategy(binary_config).get()
    binary_content = DataCache().get(binary_output["key"])
    with open(path / "sample_1280_853.jpeg", "rb") as binary_file:
        assert binary_content == binary_file.read()

    # Test text file download
    text_config = ResourceConfig(
        downloadUrl=url + "/sample2.json",
        mediaType="application/json",
    )
    text_output = FileStrategy(text_config).get()
    text_content = DataCache().get(text_output["key"]).decode()
    with open(
        path / "sample2.json", mode="rt", encoding="utf-8", newline=""
    ) as text_file:
        assert text_content == text_file.read()
