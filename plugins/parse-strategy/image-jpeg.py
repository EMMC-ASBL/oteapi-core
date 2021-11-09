""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

from PIL import Image

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


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
        self.localpath = "/app/data"
        self.filename = self.resource_config.downloadUrl.path.rsplit("/", 1)[-1]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(
        self, session: Optional[Dict[str, Any]] = None
    ) -> Dict:  # pylint: disable=W0613
        """Initialize"""
        return dict()

    def parse(
        self, session: Optional[Dict[str, Any]] = None
    ) -> Dict:  # pylint: disable=W0613
        self.conf.update(session)
        print("### Updated", self.conf)
        if "imagecrop" in self.conf:
            print("cropping!")
            im = Image.open(f"{self.localpath}/{self.filename}")
            crop = self.conf["imagecrop"]
            im_cropped = im.crop(tuple(crop))
            cropped_filename = f"{self.localpath}/cropped_{self.filename}"
            im_cropped = im_cropped.save(cropped_filename)
            return dict(filename=cropped_filename)
        return dict(status="ok")
