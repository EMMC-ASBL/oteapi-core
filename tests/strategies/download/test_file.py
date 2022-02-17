"""Tests the download strategy for 'file://'."""


def test_file():
    """Test `file` download strategy on 'sample_1280_853.jpeg' and
    'sample2.json', downloaded from filesamples.com.
    """
    from pathlib import Path

    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.file import FileStrategy

    path = Path(__file__).resolve().parent

    # Test binary file download
    binary_config = ResourceConfig(
        downloadUrl=(path / "sample_1280_853.jpeg").as_uri(),
        mediaType="image/jpeg",
    )
    binary_output = FileStrategy(binary_config).get()
    binary_content = DataCache().get(binary_output["key"])
    assert binary_content == (path / "sample_1280_853.jpeg").read_bytes()

    # Test text file download
    text_config = ResourceConfig(
        downloadUrl=(path / "sample2.json").as_uri(),
        mediaType="application/json",
    )
    text_output = FileStrategy(text_config).get()
    text_content = DataCache().get(text_output["key"]).decode()
    with open(
        path / "sample2.json", mode="rt", encoding="utf-8", newline=""
    ) as text_file:
        assert text_content == text_file.read()
