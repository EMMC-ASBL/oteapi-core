 #pylint: disable=W0613, W0511
""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy import factory
from app.models.resourceconfig import ResourceConfig
from typing import Dict, Optional, Any
import requests

@dataclass
class HTTPSStrategy:

    resource_config: ResourceConfig


    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Download via http/https and store on local cache """
        req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
        path = self.resource_config.downloadUrl.path
        filename = path.rsplit('/', 1)[-1] # Extract filename
        filepath = f'/app/data/{filename}' # TODO: Use configurable cache storage location
        with open (filepath, 'wb') as output:
            output.write(req.content)
            return dict(filename=filepath)

        return {}

def initialize() -> None:
    """ register download strategy """
    factory.register_download_strategy("https", HTTPSStrategy)
    factory.register_download_strategy("http", HTTPSStrategy)