"""Tests the parse strategy for JPEG."""
import os
from pathlib import Path


def test_jpeg(import_oteapi_modules):
    """Test `image/jpeg` parse strategy on 'sample_1280_853.jpeg',
    downloaded from filesamples.com (called 'sample_1280x853.jpeg').
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image_jpeg import ImageDataParseStrategy

    thisDir = Path(__file__).resolve().parent
    parentDir = thisDir.parent
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/jpeg",
        configuration={
            "localpath": str(parentDir),
            "filename": "sample_1280_853.jpeg",
            "crop": (200, 300, 900, 700),
        }
    )
    parser = ImageDataParseStrategy(config)
    parser.parse()

    with open(thisDir / "sample_700_400.jpeg", "rb") as f:
        target_data = f.read()
    with open(parentDir / "cropped_sample_1280_853.jpeg", "rb") as f2:
        cropped_data = f2.read()
    os.remove(parentDir / "cropped_sample_1280_853.jpeg")
    assert cropped_data == target_data
