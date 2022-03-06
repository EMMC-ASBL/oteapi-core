"""Tests the crop filter strategy."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from oteapi.interfaces import IFilterStrategy, IParseStrategy


def test_crop_filter(static_files: "Path") -> None:
    """Test the crop filter strategy on a local file.

    Note: This test incorporates much of the contents of the test
    'test_jpeg.py', so if that test fails, this one should fail too.
    """
    from oteapi.datacache import DataCache
    from oteapi.strategies.filter.crop_filter import CropImageFilter
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    # Create a temporary directory to use for this test
    sample_file = static_files / "sample_1280_853.jpeg"

    crop = [200, 300, 900, 700]

    filter_config = {
        "filterType": "filter/crop",
        "configuration": {"crop": crop},
    }
    crop_filter: "IFilterStrategy" = CropImageFilter(filter_config)

    image_config = {
        "downloadUrl": sample_file.as_uri(),
        "mediaType": "image/jpeg",
    }
    image_parser: "IParseStrategy" = ImageDataParseStrategy(image_config)

    # Run "pipeline"
    session = {}
    session.update(crop_filter.initialize(session))
    session.update(image_parser.initialize(session))
    session.update(image_parser.get(session))
    session.update(crop_filter.get(session))

    cache = DataCache()
    image_key = session["image_key"]
    data = cache.get(image_key)

    assert data.shape == (400, 700, 3)

    del cache[image_key]
