"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
from enum import Enum
from typing import TYPE_CHECKING, Optional, Tuple

import numpy as np
from PIL import Image
from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class ImageParserConfig(AttrDict):
    """Configuration data model for
    [`ImageDataParseStrategy`][oteapi.strategies.parse.image.ImageDataParseStrategy]."""

    crop: Optional[Tuple[int, int, int, int]] = Field(
        None,
        description="Box cropping parameters (left, top, right, bottom).",
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )
    download_config: Optional[ResourceConfig] = Field(
        {},
        description="Configurations passed to the downloader.",
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


class ImageParserResourceConfig(ResourceConfig):
    """Image parse strategy resource config."""

    configuration: ImageParserConfig = Field(
        ImageParserConfig(),
        description="Image parse strategy-specific configuration.",
    )
    mediaType: str = Field(
        ...,
        description=(
            "The media type of the distribution as defined by IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]"
            ".\n\nUsage: This property *SHOULD* be used when the media"
            " type of the distribution is defined in IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]."
        ),
    )


class SupportedFormats(Enum):
    """Supported formats for `ImageDataParseStrategy`."""

    jpeg = "JPEG"
    jpg = "JPEG"
    jp2 = "JPEG2000"
    png = "PNG"
    gif = "GIF"
    tiff = "TIFF"
    tif = "TIFF"
    eps = "EPS"


class SessionUpdateImageParse(SessionUpdate):
    """Configuration model for ImageParse.

    For
      - image_mode
      - image_palette
      - image_info

    see [Pillow handbook](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) for more details.
    """

    image_key: str = Field(
        ...,
        description="Key with which the image content is stored in datacache.",
    )
    image_size: Tuple[int, int] = Field(
        ...,
        description="Image size (width, height).",
    )
    image_mode: str = Field(
        ...,
        description="Image mode. Examples: 'L', 'P', 'RGB', 'RGBA'...",
    )
    image_palette_key: str = Field(
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

    It also support simple cropping and image conversions.

    The key to the new array and other metadata is stored in the session. See
    [`SessionUpdateImageParse`][oteapi.strategies.parse.image.SessionUpdateImageParse]
    for more info.

    **Registers strategies**:

    - `("mediaType", "image/jpg")`
    - `("mediaType", "image/jpeg")`
    - `("mediaType", "image/jp2")`
    - `("mediaType", "image/png")`
    - `("mediaType", "image/gif")`
    - `("mediaType", "image/tiff")`
    - `("mediaType", "image/eps")`

    """

    parse_config: ImageParserResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        return SessionUpdate()

    def get(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdateImageParse:
        """Execute the strategy."""
        if not session:
            session = {}

        config = self.parse_config.configuration
        crop = config.crop if config.crop else session.get("imagecrop")

        mime_format = self.parse_config.mediaType.split("/")[1]
        image_format = SupportedFormats[mime_format].value

        # Proper download configurations
        conf = self.parse_config.dict()
        del conf["configuration"]
        if config.download_config:
            conf.update(config.download_config.dict())
        download_config = ResourceConfig(**conf)

        downloader = create_strategy("download", download_config)
        session.update(downloader.initialize(session))

        downloader = create_strategy("download", download_config)
        output = downloader.get(session)
        session.update(output)

        if config.datacache_config and config.datacache_config.accessKey:
            cache_key = config.datacache_config.accessKey
        elif "key" in output:
            cache_key = output["key"]
        else:
            RuntimeError("no datacache key provided to downloaded content")

        cache = DataCache(config.datacache_config)

        # Treat image according to filter values
        with cache.getfile(cache_key, suffix=mime_format) as filename:
            image = Image.open(filename, formats=[image_format])
            if crop:
                image = image.crop(crop)
            if config.image_mode:
                image = image.convert(mode=config.image_mode)

        if image_format == "GIF":
            if image.info.get("version", b"").startswith(b"GIF"):
                image.info.update(
                    {"version": image.info.get("version", b"")[len(b"GIF") :]}
                )

        # Use the buffer protocol to store the image in the datacache
        data = np.asarray(image)
        image_key = cache.add(data, key=config.image_key, tag=str(id(session)))

        if image.mode == "P":
            image_palette_key = cache.add(
                np.asarray(image.getpalette()), tag=str(id(session))
            )
        else:
            image_palette_key = None

        return SessionUpdateImageParse(
            image_key=image_key,
            image_size=image.size,
            image_mode=image.mode,
            image_palette_key=image_palette_key,
            image_info=image.info,
        )
