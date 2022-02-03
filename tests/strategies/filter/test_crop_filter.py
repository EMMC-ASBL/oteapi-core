"""Tests the crop filter strategy."""
import os
from pathlib import Path


def test_crop_filter(import_oteapi_modules):
    """Test the crop filter strategy on 'sample_1280_853.jpeg',
    downloaded from filesamples.com (called 'sample_1280x853').

    Note: This test incorporates much of the contents of the test
    'test_jpeg.py', so if that test fails, this one should fail too.
    """
    from oteapi.models.filterconfig import FilterConfig
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.filter.crop_filter import CropFilter
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    parent_dir = Path(__file__).resolve().parents[1]
    crop = [200, 300, 900, 700]
    filter_config = FilterConfig(
        filterType="filter/crop",
        configuration={"crop": crop},
    )
    crop_filter_data = CropFilter(filter_config).get()
    image_config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/jpeg",
        configuration={
            "localpath": str(parent_dir),
            "filename": "sample_1280_853.jpeg",
            "crop": crop_filter_data["imagecrop"],
        },
    )
    parser_jpeg = ImageDataParseStrategy(image_config)
    parser_jpeg.parse()

    with open(parent_dir / "sample_700_400.jpeg", "rb") as sample:
        target_data = sample.read()
    with open(parent_dir / "cropped_sample_1280_853.jpeg", "rb") as cropped:
        cropped_data = cropped.read()
    os.remove(parent_dir / "cropped_sample_1280_853.jpeg")
    assert cropped_data == target_data
