""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy import factory
from typing import Dict, Optional
from app.models.resourceconfig import ResourceConfig
from PIL import Image

@dataclass
class ImageDataParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = '/app/data'
        self.filename = self.resource_config.downloadUrl.path.rsplit('/', 1)[-1]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def parse(self, session_id: Optional[str] = None) -> Dict: #pylint: disable=W0613
        if 'crop' in self.conf:
            im = Image.open(f'{self.localpath}/{self.filename}')
            crop = self.conf['crop']
            im_cropped = im.crop(tuple(crop))
            cropped_filename = f'{self.localpath}/cropped_{self.filename}'
            im_cropped = im_cropped.save(cropped_filename)
            return dict(filename=cropped_filename)
        return dict(status='ok')

def initialize() -> None:
    factory.register_parse_strategy("image/jpg", ImageDataParseStrategy)
    factory.register_parse_strategy("image/jpeg", ImageDataParseStrategy)
    factory.register_parse_strategy("image/j2p", ImageDataParseStrategy)
    factory.register_parse_strategy("image/png", ImageDataParseStrategy)
    factory.register_parse_strategy("image/gif", ImageDataParseStrategy)
    factory.register_parse_strategy("image/tiff", ImageDataParseStrategy)
    factory.register_parse_strategy("image/eps", ImageDataParseStrategy)