"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING, Optional, Tuple

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
        description="Box cropping parameters.",
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )


class ImageParserResourceConfig(ResourceConfig):
    """Image parse strategy resource config."""

    configuration: ImageParserConfig = Field(
        ImageParserConfig(), description="Image parse strategy-specific configuration."
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


class SupportedFormat(Enum):
    """Supported formats for `ImageDataParseStrategy`."""

    JPEG = "JPEG"
    JPEG2000 = "JPEG2000"
    PNG = "PNG"
    GIF = "GIF"
    TIFF = "TIFF"
    EPS = "EPS"


class SessionUpdateImageParse(SessionUpdate):
    """Configuration model for ImageParse."""

    content: bytes = Field(..., description="Parsed output from ImageParse.")
    format: SupportedFormat = Field(..., description="The format of the parsed image.")
    cropped: bool = Field(..., description="Whether or not the image has been cropped.")


@dataclass
class ImageDataParseStrategy:
    """Parse strategy for images.

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
        if session:
            self._use_filters(session)
        session = session if session else {}

        mime_format = self.parse_config.mediaType.split("/")[1]
        image_format = self._map_mime_to_format()

        # Retrieve image file
        download_config = ResourceConfig(**self.parse_config.dict())
        del download_config.configuration
        downloader = create_strategy("download", download_config)
        session.update(downloader.initialize(session))
        cache_key = downloader.get(session).get("key", "")

        cache = DataCache(self.parse_config.configuration.datacache_config)

        # Treat image according to filter values
        with cache.getfile(cache_key, suffix=mime_format) as filename:
            image = Image.open(filename, formats=[image_format]).crop(
                self.parse_config.configuration.crop
            )

        if image_format == "GIF":
            if image.info.get("version", b"").startswith(b"GIF"):
                image.info.update(
                    {"version": image.info.get("version", b"")[len(b"GIF") :]}
                )

        # Return parsed and treated image
        image_content = BytesIO()
        image.save(image_content, format=image_format)
        return SessionUpdateImageParse(
            content=image_content.getvalue(),
            format=image_format,
            cropped=bool(self.parse_config.configuration.crop),
        )

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "imagecrop" in session and not self.parse_config.configuration.crop:
            # Use CropFilter available in session
            self.parse_config.configuration.crop = session["imagecrop"]

    def _map_mime_to_format(self) -> str:
        """Return mapped Pillow-understandable format."""
        image_format = self.parse_config.mediaType.split("/")[1]
        return {
            "jpg": "JPEG",
            "jp2": "JPEG2000",
        }.get(image_format, image_format.upper())
