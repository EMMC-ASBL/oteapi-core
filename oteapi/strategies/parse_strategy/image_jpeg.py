# pylint: disable=  W0613
""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.app.models.resourceconfig import ResourceConfig
from oteapi.app.strategy.factory import StrategyFactory
from PIL import Image


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

    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.resource_config.configuration["artifactName"]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
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
