"""Test the image formats in the image parse strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


image_formats = [
    ("eps", "sample_700_400.eps", "parsed_eps.eps", None, None),
    (
        "gif",
        "sample_1280_853.gif",
        "sample_700_400.gif",
        (200, 300, 900, 700),
        (400, 700),
    ),
    (
        "jpeg",
        "sample_1280_853.jpeg",
        "sample_700_400.jpeg",
        (200, 300, 900, 700),
        (400, 700),
    ),
    (
        "jpg",
        "sample_1280_853.jpg",
        "sample_700_400.jpeg",
        (200, 300, 900, 700),
        (400, 700),
    ),
    ("jp2", "sample1_1000_1000.jp2", None, None, None),
    (
        "png",
        "sample_640_426.png",
        "sample_350_250.png",
        (100, 50, 450, 300),
        (250, 350),
    ),
    (
        "tiff",
        "sample_640_426.tiff",
        "sample_350_250.tiff",
        (100, 50, 450, 300),
        (250, 350),
    ),
    ("gif", "sample_700_400.gif", None, None, None),
]


@pytest.mark.parametrize(
    ("image_format", "filename", "filename_cropped", "crop", "cropped_size"),
    image_formats,
    ids=[_[0] for _ in image_formats[:-1]] + [f"{image_formats[-1][0]}-no crop"],
)
def test_image(
    image_format: str,
    filename: str,
    filename_cropped: str | None,
    crop: tuple[int, int, int, int] | None,
    cropped_size: tuple[int, int] | None,
    static_files: Path,
) -> None:
    """Test parsing an image format."""
    import numpy as np
    from PIL import Image

    from oteapi.datacache import DataCache
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    if image_format == "eps":
        # Skip if Ghostscript is not installed
        import platform
        import subprocess

        command = {
            "Linux": ["gs -h"],
            "Windows": [
                "gswin32.exe -h",
                "gswin32c.exe -h",
                "gswin64.exe -h",
                "gswin64c.exe -h",
            ],
        }.get(platform.system(), None)

        if not command:
            raise RuntimeError(
                f"No support for testing EPS image parser with OS {platform.system()}"
            )

        failed = True
        for cmd in command:
            try:
                subprocess.run(cmd.split(), check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            else:
                failed = False

        if failed:
            pytest.skip("Could not find Ghostscript on the system.")

    sample_file = static_files / filename
    reference_file = (
        static_files / filename_cropped if filename_cropped else static_files / filename
    )
    assert sample_file.exists(), f"Test file not found at {sample_file} !"
    assert reference_file.exists(), f"Test file not found at {reference_file} !"

    for itest in range(2):
        print(f"crop from cropfilter (itest) = {'true' if itest else 'false'}")
        # Test with and without mocking the crop filter strategy.
        key = "imagecrop" if itest else "crop"
        crop_config = {key: crop} if crop else {}
        config = {
            "parserType": "parser/image",
            "entity": "http://onto-ns.com/meta/0.4/example_iri",
            "configuration": {
                "downloadUrl": sample_file.as_uri(),
                "mediaType": f"image/{image_format}",
                **crop_config,
            },
        }

        output = ImageDataParseStrategy(parse_config=config).get()

        cache = DataCache()
        image_key = output["image_key"]
        try:
            data = cache.get(image_key)
        finally:
            del cache[image_key]

        data = np.asarray(
            Image.frombytes(
                data=data, mode=output["image_mode"], size=output["image_size"]
            )
        )

        if crop:
            mode = output["image_mode"]
            assert data.shape == (cropped_size if mode == "P" else (*cropped_size, 3))

    if filename_cropped and image_format in ("png", "gif", "eps", "tiff"):
        with Image.open(reference_file, formats=[image_format]) as cropped:
            arr = np.asarray(cropped)
            assert np.all(data == arr)


@pytest.mark.parametrize("crop", [None, (100, 50, 450, 300)], ids=["no crop", "crop"])
def test_initialize_returns_nothing(
    crop: tuple[int, int, int, int] | None,
) -> None:
    """Assert that the initialize method returns nothing."""
    from oteapi.models.genericconfig import AttrDict
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    config = {
        "parserType": "parser/image",
        "entity": "http://onto-ns.com/meta/0.4/example_iri",
        "configuration": {
            "downloadUrl": "https://example.org",
            "mediaType": "image/jpeg",
            "imagecrop": crop,
        },
    }
    parser = ImageDataParseStrategy(parse_config=config)
    assert parser.initialize() == AttrDict()
