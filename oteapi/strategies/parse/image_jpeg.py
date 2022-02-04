"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


@dataclass
class ImageDataParseStrategy:
    """Parse strategy for images.

    **Registers strategies**:

    - `("mediaType", "image/jpg")`
    - `("mediaType", "image/jpeg")`
    - `("mediaType", "image/j2p")`
    - `("mediaType", "image/png")`
    - `("mediaType", "image/gif")`
    - `("mediaType", "image/tiff")`
    - `("mediaType", "image/eps")`

    """

    parse_config: "ResourceConfig"

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.parse_config.configuration["artifactName"]
        if self.parse_config.configuration:
            self.conf = self.parse_config.configuration
        else:
            self.conf = {}

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
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
        return parsedOutput
