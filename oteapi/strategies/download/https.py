"""Download strategy class for http/https"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

from oteapi.datacache import DataCache
from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(("scheme", "http"), ("scheme", "https"))
class HTTPSStrategy:
    """Strategy for retrieving data via http.

    **Registers strategies**:

    - `("scheme", "http")`
    - `("scheme", "https")`

    """

    resource_config: "ResourceConfig"

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, **_) -> "Dict[str, Any]":
        """Download via http/https and store on local cache."""
        cache = DataCache(self.resource_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            if not self.resource_config.downloadUrl:
                raise ValueError("downloadUrl not defined in configuration.")
            req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
            key = cache.add(req.content)

        return {"key": key}
