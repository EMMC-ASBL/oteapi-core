"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
import sys
from enum import Enum
from typing import TYPE_CHECKING, Optional, Tuple

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

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
    download_config: AttrDict = Field(
        AttrDict(),
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

    mediaType: Literal[
        "image/jpg",
        "image/jpeg",
        "image/jp2",
        "image/png",
        "image/gif",
        "image/tiff",
        "image/eps",
    ] = Field(
        ...,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: ImageParserConfig = Field(
        ImageParserConfig(),
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


class SessionUpdateImageParse(SessionUpdate):
    """Configuration model for ImageParse.

    See [Pillow handbook](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) for more details
    on `image_mode`, `image_palette`, and `image_info`.
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
        image_format = SupportedFormat[mime_format].value

        # Proper download configurations
        conf = self.parse_config.dict()
        conf["configuration"] = config.download_config or {}
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
            raise RuntimeError("No data cache key provided to the downloaded content")

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
            image_key = cache.add(
                data,
                key=config.image_key,
                tag=str(id(session)),
            )

            if image.mode == "P":
                image_palette_key = cache.add(
                    np.asarray(image.getpalette()), tag=str(id(session))
                )
            else:
                image_palette_key = None

            # The session must be json serialisable - filter out all
            # non-json serialisable fields in image.info
            if image.info:
                image_info = {
                    key: val
                    for key, val in image.info.items()
                    if isinstance(val, (str, int, float, type(None), bool, tuple, list))
                }
            else:
                image_info = {}

            session_update = SessionUpdateImageParse(
                image_key=image_key,
                image_size=image.size,
                image_mode=image.mode,
                image_palette_key=image_palette_key,
                image_info=image_info,
            )

            # Explicitly close the image to avoid crashes on Windows
            image.close()

        return session_update
