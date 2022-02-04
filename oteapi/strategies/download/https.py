"""Download strategy class for http/https"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

from oteapi.datacache import DataCache

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


@dataclass
class HTTPSStrategy:
    """Strategy for retrieving data via http.

    **Registers strategies**:

    - `("scheme", "http")`
    - `("scheme", "https")`

    """

    download_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Download via http/https and store on local cache."""
        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            if not self.download_config.downloadUrl:
                raise ValueError("downloadUrl not defined in configuration.")
            req = requests.get(self.download_config.downloadUrl, allow_redirects=True)
            key = cache.add(req.content)

        return {"key": key}
