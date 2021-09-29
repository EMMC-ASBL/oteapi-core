""" Strategy class for image/jpg """

#from dataclasses import dataclass
from app import factory
from typing import Dict
import requests

#@dataclass
class HTTPSStrategy:
    def __init__(self, **kwargs):
        self.uri = kwargs.get('url')
        self.path = kwargs.get('path')
        self.config = kwargs.get('configuration')


    def read(self) -> Dict:
        """ Download via http/https and store on local cache """
        req = requests.get(self.uri, allow_redirects=True)
        filename = self.path.rsplit('/', 1)[-1] # Extract filename
        filepath = f'/app/data/{filename}' # TODO: Use configurable cache storage location
        with open (filepath, 'wb') as output:
            output.write(req.content)
            return dict(filename=filepath)

        return {}

def initialize() -> None:
    """ register download strategy """
    factory.register_download_strategy("https", HTTPSStrategy)
    factory.register_download_strategy("http", HTTPSStrategy)