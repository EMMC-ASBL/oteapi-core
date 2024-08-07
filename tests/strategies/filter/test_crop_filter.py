"""Tests the crop filter strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_crop_filter(static_files: Path) -> None:
    """Test the crop filter strategy on a local file.

    Note: This test incorporates much of the contents of the test
    'test_jpeg.py', so if that test fails, this one should fail too.
    """
    from copy import deepcopy

    import numpy as np
    from PIL import Image

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

    image_config = {
        "parserType": "parser/image",
        "entity": "http://onto-ns.com/meta/0.4/example_iri",
        "configuration": {
            "downloadUrl": sample_file.as_uri(),
            "mediaType": "image/jpeg",
        },
    }

    # Run pipeline = image_parser > crop_filter
    session = {}

    session.update(CropImageFilter(filter_config=filter_config).initialize())

    (pipeline_image_config := deepcopy(image_config))["configuration"].update(session)
    session.update(
        ImageDataParseStrategy(parse_config=pipeline_image_config).initialize()
    )

    (pipeline_image_config := deepcopy(image_config))["configuration"].update(session)
    session.update(ImageDataParseStrategy(parse_config=pipeline_image_config).get())

    (pipeline_filter_config := deepcopy(image_config))["configuration"].update(session)
    session.update(CropImageFilter(filter_config=pipeline_filter_config).get())

    cache = DataCache()
    image_key = session["image_key"]

    try:
        data = cache.get(image_key)
    finally:
        del cache[image_key]

    data = np.asarray(
        Image.frombytes(
            data=data, mode=session["image_mode"], size=session["image_size"]
        )
    )
    assert data.shape == (400, 700, 3)
