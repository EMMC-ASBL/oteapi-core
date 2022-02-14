"""Tests the crop filter strategy."""
from shutil import copy


def test_crop_filter(tmp_path):
    """Test the crop filter strategy on 'sample_1280_853.jpeg',
    downloaded from filesamples.com (called 'sample_1280x853').

    Note: This test incorporates much of the contents of the test
    'test_jpeg.py', so if that test fails, this one should fail too.
    """
    from pathlib import Path

    from oteapi.models.filterconfig import FilterConfig
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.filter.crop_filter import CropFilter
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    parent_dir = Path(__file__).resolve().parents[1]
    # Create a temporary directory to use for this test
    source_file = "sample_1280_853.jpeg"
    copy(parent_dir / source_file, tmp_path / source_file)

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
            "localpath": str(tmp_path),
            "filename": source_file,
            "crop": crop_filter_data.crop,
        },
    )
    ImageDataParseStrategy(image_config).get()

    cropped_file = tmp_path / f"cropped_{source_file}"
    cropped_data = cropped_file.read_bytes()
    assert cropped_data == (parent_dir / "sample_700_400.jpeg").read_bytes()
