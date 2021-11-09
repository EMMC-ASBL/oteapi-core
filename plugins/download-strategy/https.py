# pylint: disable=W0613, W0511
""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("scheme", "http"), ("scheme", "https"))
class HTTPSStrategy:

    resource_config: ResourceConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Download via http/https and store on local cache"""
        req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
        path = self.resource_config.downloadUrl.path
        filename = path.rsplit("/", 1)[-1]  # Extract filename
        print(f"-> PATH = {path}")
        filepath = (
            f"/app/data/{filename}"  # TODO: Use configurable cache storage location
        )
        print(f"-> STORING AT {filepath}")
        with open(filepath, "wb") as output:
            output.write(req.content)
            return dict(filename=filepath)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Download via http/https and store on local cache"""
        req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
        path = self.resource_config.downloadUrl.path
        filename = path.rsplit("/", 1)[-1]  # Extract filename
        print(f"-> PATH = {path}")
        filepath = (
            f"/app/data/{filename}"  # TODO: Use configurable cache storage location
        )
        print(f"-> STORING AT {filepath}")
        with open(filepath, "wb") as output:
            output.write(req.content)
            return dict(filename=filepath)
