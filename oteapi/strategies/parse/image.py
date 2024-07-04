"""Strategy class for image/jpg."""

import sys
from enum import Enum
from typing import Optional, Tuple

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

from PIL import Image
from pydantic import AliasChoices, Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ParserConfig, ResourceConfig
from oteapi.models.resourceconfig import HostlessAnyUrl
from oteapi.plugins import create_strategy


class ImageConfig(AttrDict):
    """Configuration data model for
    [`ImageDataParseStrategy`][oteapi.strategies.parse.image.ImageDataParseStrategy]."""

    # Resource config
    downloadUrl: Optional[HostlessAnyUrl] = Field(
        None, description=ResourceConfig.model_fields["downloadUrl"].description
    )
    mediaType: Optional[
        Literal[
            "image/jpg",
            "image/jpeg",
            "image/jp2",
            "image/png",
            "image/gif",
            "image/tiff",
            "image/eps",
        ]
    ] = Field(
        None,
        description=ResourceConfig.model_fields["mediaType"].description,
    )

    # Image parse strategy-specific config
    crop: Optional[Tuple[int, int, int, int]] = Field(
        None,
        description="Box cropping parameters (left, top, right, bottom).",
        # Effectively mapping 'imagecrop' to 'crop'.
        # 'imagecrop' is used by the crop filter strategy.
        validation_alias=AliasChoices("crop", "imagecrop"),
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )
    image_key: Optional[str] = Field(
        None,
        description="Key to use when storing the image data in datacache.",
    )
    image_mode: Optional[str] = Field(
        None,
        description=(
            "Pillow mode to convert image into. See "
            "https://pillow.readthedocs.io/en/stable/handbook/concepts.html "
            "for details."
        ),
    )


class ImageParserConfig(ParserConfig):
    """Image parse strategy resource config."""

    parserType: Literal["parser/image"] = Field(
        "parser/image",
        description=ParserConfig.model_fields["parserType"].description,
    )
    configuration: ImageConfig = Field(
        ...,
        description="Image parse strategy-specific configuration.",
    )


class SupportedFormat(Enum):
    """Supported formats for `ImageDataParseStrategy`."""

    jpeg = "JPEG"
    jpg = "JPEG"
    jp2 = "JPEG2000"
    png = "PNG"
    gif = "GIF"
    tiff = "TIFF"
    eps = "EPS"


class ImageParseContent(AttrDict):
    """Configuration model for the returned content from the Image parser.

    See
    [Pillow handbook](https://pillow.readthedocs.io/en/stable/handbook/concepts.html)
    for more details on `image_mode`, `image_palette`, and `image_info`.
    """

    image_key: str = Field(
        ...,
        description="Key with which the image content is stored in the data cache.",
    )
    image_size: Tuple[int, int] = Field(
        ...,
        description="Image size (width, height).",
    )
    image_mode: str = Field(
        ...,
        description="Image mode. Examples: 'L', 'P', 'RGB', 'RGBA'...",
    )
    image_palette_key: Optional[str] = Field(
        None,
        description="Datacache key for colour palette if mode is 'P'.",
    )
    image_info: dict = Field(
        {},
        description="Additional information about the image.",
    )


@dataclass
class ImageDataParseStrategy:
    """Parse strategy for images.

    This strategy uses Pillow to read a raw image from the data cache,
    converts it into a NumPy array and stores the new array in the
    data cache.

    It also supports simple cropping and image conversions.

    The key to the new array and other metadata is returned. See
    [`ImageParseContent`][oteapi.strategies.parse.image.ImageParseContent]
    for more info.

    """

    parse_config: ImageParserConfig

    def initialize(self) -> AttrDict:
        """Initialize strategy."""
        return AttrDict()

    def get(self) -> ImageParseContent:
        """Execute the strategy."""

        config = self.parse_config.configuration

        if config.mediaType is None:
            raise ValueError("No media type provided to the image parser")

        mime_format = config.mediaType.split("/")[1]
        image_format = SupportedFormat[mime_format].value

        # Download the image
        download_config = config.model_dump()
        download_config["configuration"] = config.model_dump()
        output = create_strategy("download", download_config).get()

        if config.datacache_config and config.datacache_config.accessKey:
            cache_key = config.datacache_config.accessKey
        elif "key" in output:
            cache_key = output["key"]
        else:
            raise RuntimeError("No data cache key provided to the downloaded content")

        cache = DataCache(config.datacache_config)

        # Treat image according to filter values
        with (
            cache.getfile(cache_key, suffix=mime_format) as filename,
            Image.open(filename, formats=[image_format]) as image,
        ):
            if config.crop:
                image = image.crop(config.crop)
            if config.image_mode:
                image = image.convert(mode=config.image_mode)

            if image_format == "GIF" and image.info.get("version", b"").startswith(
                b"GIF"
            ):
                image.info.update(
                    {"version": image.info.get("version", b"")[len(b"GIF") :]}
                )

            image_key = cache.add(
                image.tobytes(),
                key=config.image_key,
            )

            if image.mode == "P":
                image_palette_key = cache.add(image.getpalette())
            else:
                image_palette_key = None

            # The returned content must be json serialisable - filter out all
            # non-json serialisable fields in image.info
            if image.info:
                image_info = {
                    key: val
                    for key, val in image.info.items()
                    if isinstance(val, (str, int, float, type(None), bool, tuple, list))
                }
            else:
                image_info = {}

            content = ImageParseContent(
                image_key=image_key,
                image_size=image.size,
                image_mode=image.mode,
                image_palette_key=image_palette_key,
                image_info=image_info,
            )

        return content
