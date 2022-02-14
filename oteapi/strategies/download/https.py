"""Download strategy class for http/https"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests
from pydantic import Field

from oteapi.datacache import DataCache
from oteapi.models import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


class SessionUpdateHTTPS(SessionUpdate):
    """Class for returning values from Download HTTPS strategy."""

    key: str = Field(..., description="Key to access the data in the cache.")


@dataclass
class HTTPSStrategy:
    """Strategy for retrieving data via http.

    **Registers strategies**:

    - `("scheme", "http")`
    - `("scheme", "https")`

    """

    download_config: "ResourceConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateHTTPS:
        """Download via http/https and store on local cache."""
        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            if not self.download_config.downloadUrl:
                raise ValueError("downloadUrl not defined in configuration.")
            req = requests.get(self.download_config.downloadUrl, allow_redirects=True)
            key = cache.add(req.content)

        return SessionUpdateHTTPS(key=key)
