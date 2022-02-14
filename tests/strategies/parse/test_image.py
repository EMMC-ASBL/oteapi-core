"""Test the image formats in the image parse strategy."""
# pylint: disable=too-many-locals
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional, Tuple

    from oteapi.interfaces.iparsestrategy import IParseStrategy


image_formats = [
    ("eps", "sample_700_400.eps", "parsed_eps.eps", None),
    ("gif", "sample_1280_853.gif", "sample_700_400.gif", (200, 300, 900, 700)),
    ("jpeg", "sample_1280_853.jpeg", "sample_700_400.jpeg", (200, 300, 900, 700)),
    ("jpg", "sample_1280_853.jpg", "sample_700_400.jpeg", (200, 300, 900, 700)),
    ("jp2", "sample1.jp2", "sample1_1000_1000.jp2", (1000, 1000, 2000, 2000)),
    ("png", "sample_640_426.png", "sample_350_250.png", (100, 50, 450, 300)),
    ("tiff", "sample_640_426.tiff", "sample_350_250.tiff", (100, 50, 450, 300)),
    ("gif", "sample_700_400.gif", None, None),
]


@pytest.mark.parametrize(
    "image_format,filename,filename_cropped,crop",
    image_formats,
    ids=[_[0] for _ in image_formats[:-1]] + [f"{image_formats[-1][0]}-no crop"],
)
def test_image(
    image_format: str,
    filename: str,
    filename_cropped: "Optional[str]",
    crop: "Optional[Tuple[int, int, int, int]]",
    static_files: "Path",
) -> None:
    """Test parsing an image format."""
    from oteapi.strategies.parse.image import ImageDataParseStrategy, SupportedFormat

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
            except subprocess.CalledProcessError:
                pass
            else:
                failed = False

        if failed:
            pytest.skip("Could not find Ghostscript on the system.")

    mime_to_format = {"jpg": "jpeg", "jp2": "jpeg2000"}

    sample_file = static_files / filename
    reference_file = (
        static_files / filename_cropped if filename_cropped else static_files / filename
    )
    assert sample_file.exists(), f"Test file not found at {sample_file} !"
    assert reference_file.exists(), f"Test file not found at {reference_file} !"

    for config_parse_test in range(2):
        print(f"config_parse_test={config_parse_test}")

        config = {
            "downloadUrl": sample_file.as_uri(),
            "mediaType": f"image/{image_format}",
            "configuration": {"crop": crop} if crop and config_parse_test == 0 else {},
        }
        parser: "IParseStrategy" = ImageDataParseStrategy(parse_config=config)

        session = parser.initialize(
            {"imagecrop": crop} if crop and config_parse_test == 1 else None
        )
        session = parser.get(
            {"imagecrop": crop} if crop and config_parse_test == 1 else session
        )

        assert (
            session.get("cropped", False) if crop else not session.get("cropped", False)
        )
        assert (
            session.get("format", SupportedFormat).value
            == mime_to_format.get(image_format, image_format).upper()
        )
        assert session.get("content", b"") == reference_file.read_bytes()
