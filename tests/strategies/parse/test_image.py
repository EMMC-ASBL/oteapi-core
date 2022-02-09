"""Test the image formats in the image parse strategy."""
from pathlib import Path
from typing import Tuple

import pytest


def get_cropping_values(ext: str) -> Tuple[int]:
    """Return the cropping values for the test."""
    croppings = {
        "gif": (200, 300, 900, 700),
        "jpeg": (200, 300, 900, 700),
        "jpg": (200, 300, 900, 700),
        "jp2": (1000, 1000, 2000, 2000),
        "png": (100, 50, 450, 300),
        "tiff": (100, 50, 450, 300),
    }
    return croppings[ext]


def get_orig_path(ext: str) -> Path:
    """Return the path to the original image in the test."""
    dirs = Path(__file__).resolve().parents
    origs = {
        "gif": dirs[0] / "sample_1280_853.gif",
        "jpeg": dirs[1] / "sample_1280_853.jpeg",
        "jpg": dirs[1] / "sample_1280_853.jpg",
        "jp2": dirs[0] / "sample1.jp2",
        "png": dirs[0] / "sample_640_426.png",
        "tiff": dirs[0] / "sample_640_426.tiff",
    }
    return origs[ext]


def get_target_path(ext: str) -> Path:
    """Return the path to the target contents for the cropped image
    in the test.
    """
    dirs = Path(__file__).resolve().parents
    targets = {
        "gif": dirs[0] / "sample_700_400.gif",
        "jpeg": dirs[1] / "sample_700_400.jpeg",
        "jpg": dirs[1] / "sample_700_400.jpeg",
        "jp2": dirs[0] / "sample1_1000_1000.jp2",
        "png": dirs[0] / "sample_350_250.png",
        "tiff": dirs[0] / "sample_350_250.tiff",
    }
    return targets[ext]


@pytest.mark.parametrize(
    "formats",
    ["gif", "jpeg", "jpg", "jp2", "png", "tiff"],
)
def test_image(formats) -> None:
    """Test parsing an image format."""
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.image import ImageDataParseStrategy

    path = get_orig_path(formats)
    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="image/" + formats,
        configuration={
            "localpath": str(path.parent),
            "filename": path.name,
            "crop": get_cropping_values(formats),
        },
    )
    parser = ImageDataParseStrategy(config)
    parser.get()
    cropped_path = path.with_name("cropped_" + path.name)
    assert cropped_path.is_file()
    cropped_content = cropped_path.read_bytes()
    cropped_path.unlink()
    assert cropped_content == get_target_path(formats).read_bytes()
