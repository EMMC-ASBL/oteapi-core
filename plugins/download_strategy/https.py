# pylint: disable=W0613
"""Download strategy class for http/https"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from app.cache.cache import DataCache
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("scheme", "http"), ("scheme", "https"))
class HTTPSStrategy:
    """Strategy for retrieving data via http."""

    resource_config: ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Download via http/https and store on local cache."""
        cache = DataCache(self.resource_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
            key = cache.add(req.content)

        return {"key": key}
