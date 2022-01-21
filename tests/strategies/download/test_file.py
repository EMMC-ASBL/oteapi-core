"""Tests the download strategy for 'file://'."""
from pathlib import Path


def test_file(import_oteapi_modules):
    """Test `file` download strategy on 'sample_1280_853.jpeg' and
    'sample2.json', downloaded from filesamples.com.
    """
    from oteapi.strategies.download.file import FileStrategy
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.datacache.datacache import DataCache

    path = Path(__file__).resolve().parents[1]
    binaryfile = path / "sample_1280_853.jpeg"
    binaryUri = binaryfile.as_uri()
    textfile = path / "sample2.json"
    textUri = textfile.as_uri()
    # The uris now start with "file:///..." (incompatible with AnyUrl)
    # On Windows, the drive is also present, e.g. "file:///C:/...",
    # so the second ":" must be removed to produce valid AnyUrls
    binaryUrl = binaryUri.replace(":", "").replace("///", "://")
    textUrl = textUri.replace(":", "").replace("///", "://")

    # Test binary file download
    binaryConfig = ResourceConfig(
        downloadUrl=binaryUrl,
        mediaType="image/jpeg",
    )
    binaryDownloader = FileStrategy(binaryConfig)
    binaryOutput = binaryDownloader.get()
    binaryContent = DataCache().get(binaryOutput["key"])
    with open(binaryfile, "rb") as bf:
        binaryTargetContent = bf.read()
    assert binaryContent == binaryTargetContent

    # Test text file download
    textConfig = ResourceConfig(
        downloadUrl=textUrl,
        mediaType="application/json",
    )
    textDownloader = FileStrategy(textConfig)
    textOutput = textDownloader.get()
    textContent = DataCache().get(textOutput["key"]).decode()
    with open(textfile, "rt", newline="") as tf:
        textTargetContent = tf.read()
    assert textContent == textTargetContent
