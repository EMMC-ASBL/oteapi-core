"""Tests the parse strategy for GIF."""
# pylint: disable=unused-argument
import os
from pathlib import Path


def test_gif(import_oteapi_modules):
    """Test the `image/gif` parse strategy on 'sample_1280_853.gif',
    downloaded from filesamples.com (called 'sample_1280x853.gif').
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    this_dir = Path(__file__).resolve().parent
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/gif",
        configuration={
            "localpath": str(this_dir),
            "filename": "sample_1280_853.gif",
            "crop": (200, 300, 900, 700),
        },
    )
    parser = ImageDataParseStrategy(config)
    parser.parse()

    with open(this_dir / "sample_700_400.gif", "rb") as target:
        target_data = target.read()
    with open(this_dir / "cropped_sample_1280_853.gif", "rb") as cropped:
        cropped_data = cropped.read()
    os.remove(this_dir / "cropped_sample_1280_853.gif")
    assert cropped_data == target_data
