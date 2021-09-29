""" Strategy class for image/jpg """

from app import factory
from typing import Dict
from PIL import Image

class JPEGDataParseStrategy:
    def __init__(self, **kwargs):
        self.localpath = '/app/data'
        self.path = kwargs.get('path')
        self.filename = filename = self.path.rsplit('/', 1)[-1]
        self.conf = kwargs.get('configuration')


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