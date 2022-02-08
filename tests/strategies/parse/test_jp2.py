"""Tests the parse strategy for JPEG 2000."""
import os
from pathlib import Path


def test_jp2():
    """Test the `image/jp2` parse strategy on 'sample1_1000_1000.jp2,
    a cropped subset of 'sample1.jp2' downloaded from filesamples.com.
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    this_dir = Path(__file__).resolve().parent
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/jp2",
        configuration={
            "localpath": str(this_dir),
            "filename": "sample1.jp2",
            "crop": (1000, 1000, 2000, 2000),
        },
    )
    parser = ImageDataParseStrategy(config)
    parser.get()

    with open(this_dir / "sample1_1000_1000.jp2", "rb") as target:
        target_data = target.read()
    with open(this_dir / "cropped_sample1.jp2", "rb") as cropped:
        cropped_data = cropped.read()
    os.remove(this_dir / "cropped_sample1.jp2")
    assert cropped_data == target_data
