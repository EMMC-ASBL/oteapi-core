""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy import factory
from typing import Dict
from app.models.resourceconfig import ResourceConfig
from PIL import Image

@dataclass
class JPEGDataParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self, **kwargs):
        self.localpath = '/app/data'        
        self.filename = self.resource_config.accessUrl.path.rsplit('/', 1)[-1]

    def parse(self) -> Dict:
        if 'crop' in self.conf:
            im = Image.open(f'{self.localpath}/{self.filename}')
            crop = self.conf['crop']
            im_cropped = im.crop(tuple(crop))
            cropped_filename = f'{self.localpath}/cropped_{self.filename}'
            im_cropped = im_cropped.save(cropped_filename)
            return dict(filename=cropped_filename)
        return dict(status='ok')

def initialize() -> None:
    factory.register_parse_strategy("image/jpg", JPEGDataParseStrategy)
    factory.register_parse_strategy("image/jpeg", JPEGDataParseStrategy)