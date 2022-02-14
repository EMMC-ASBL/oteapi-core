"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from PIL import Image
from pydantic import Field

from oteapi.models.sessionupdate import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional

    from oteapi.models import ResourceConfig


class SessionUpdateImageParse(SessionUpdate):
    """Configuration model for ImageParse."""

    parsedOutput: Dict[str, str] = Field(
        ..., description="Parsed output from ImageParse."
    )


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

    parse_config: "ResourceConfig"

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.parse_config.configuration["filename"]
        self.conf = self.parse_config.configuration
        if "localpath" in self.conf:
            self.localpath = self.conf["localpath"]

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdateImageParse:
        if session is not None:
            self.conf.update(session)
        parsedOutput = {}
        if "crop" in self.conf:
            print("cropping!")
            im = Image.open(f"{self.localpath}/{self.filename}")
            crop = self.conf["crop"]
            im_cropped = im.crop(tuple(crop))
            cropped_filename = f"{self.localpath}/cropped_{self.filename}"
            im_cropped.save(cropped_filename)
            parsedOutput["cropped_filename"] = cropped_filename
        parsedOutput["parseImage"] = "Done"
        return SessionUpdateImageParse(parsedOutput=parsedOutput)
