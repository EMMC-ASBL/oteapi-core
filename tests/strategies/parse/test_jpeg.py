"""Tests the parse strategy for JPEG."""
import os
from pathlib import Path


def test_jpeg_jpg():
    """Test the `image/jpeg` and `image/jpg` parse strategies on
    'sample_1280_853.jpeg' and 'sample_1280_853.jpg',
    downloaded from filesamples.com (called 'sample_1280x853').

    These two files are identical, so this test tests both files
    only to test recognition of both media types.
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    parent_dir = Path(__file__).resolve().parents[1]
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/jpeg",
        configuration={
            "localpath": str(parent_dir),
            "filename": "sample_1280_853.jpeg",
            "crop": (200, 300, 900, 700),
        },
    )
    parser_jpeg = ImageDataParseStrategy(config)
    parser_jpeg.get()
    config.configuration["filename"] = "sample_1280_853.jpg"
    parser_jpg = ImageDataParseStrategy(config)
    parser_jpg.get()

    with open(parent_dir / "sample_700_400.jpeg", "rb") as sample:
        target_data = sample.read()
    with open(parent_dir / "cropped_sample_1280_853.jpeg", "rb") as cropped:
        cropped_jpeg_data = cropped.read()
    with open(parent_dir / "cropped_sample_1280_853.jpg", "rb") as cropped:
        cropped_jpg_data = cropped.read()
    os.remove(parent_dir / "cropped_sample_1280_853.jpeg")
    os.remove(parent_dir / "cropped_sample_1280_853.jpg")
    assert cropped_jpeg_data == cropped_jpg_data == target_data
