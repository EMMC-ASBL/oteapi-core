"""Strategy class for image/jpg."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PIL import Image

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(
    ("mediaType", "image/jpg"),
    ("mediaType", "image/jpeg"),
    ("mediaType", "image/j2p"),
    ("mediaType", "image/png"),
    ("mediaType", "image/gif"),
    ("mediaType", "image/tiff"),
    ("mediaType", "image/eps"),
)
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

    resource_config: "ResourceConfig"

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.resource_config.configuration["artifactName"]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def parse(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
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
