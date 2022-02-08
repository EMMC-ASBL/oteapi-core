"""Tests the parse strategy for PNG."""
import os
from pathlib import Path


def test_png():
    """Test the `image/png` parse strategy on 'sample_640_426.png',
    downloaded from filesamples.com (called 'sample_640x426.png').
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    this_dir = Path(__file__).resolve().parent
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/png",
        configuration={
            "localpath": str(this_dir),
            "filename": "sample_640_426.png",
            "crop": (100, 50, 450, 300),
        },
    )
    parser = ImageDataParseStrategy(config)
    parser.get()

    with open(this_dir / "sample_350_250.png", "rb") as target:
        target_data = target.read()
    with open(this_dir / "cropped_sample_640_426.png", "rb") as cropped:
        cropped_data = cropped.read()
    os.remove(this_dir / "cropped_sample_640_426.png")
    assert cropped_data == target_data
