"""Tests the parse strategy for JPEG."""
# pylint: disable=unused-argument
import os
from pathlib import Path


def test_jpeg(import_oteapi_modules):
    """Test `image/jpeg` parse strategy on 'sample_1280_853.jpeg',
    downloaded from filesamples.com (called 'sample_1280x853.jpeg').
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image_jpeg import ImageDataParseStrategy

    this_dir = Path(__file__).resolve().parent
    parent_dir = this_dir.parent
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/jpeg",
        configuration={
            "localpath": str(parent_dir),
            "filename": "sample_1280_853.jpeg",
            "crop": (200, 300, 900, 700),
        },
    )
    parser = ImageDataParseStrategy(config)
    parser.parse()

    with open(this_dir / "sample_700_400.jpeg", "rb") as sample:
        target_data = sample.read()
    with open(parent_dir / "cropped_sample_1280_853.jpeg", "rb") as cropped:
        cropped_data = cropped.read()
    os.remove(parent_dir / "cropped_sample_1280_853.jpeg")
    assert cropped_data == target_data
