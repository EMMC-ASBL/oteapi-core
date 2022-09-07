"""Download strategy class for http/https"""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Optional

import requests
from pydantic import AnyHttpUrl, Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class HTTPSConfig(AttrDict):
    """HTTP(S)-specific Configuration Data Model."""

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configurations for the data cache for storing the downloaded file content.",
    )


class HTTPSResourceConfig(ResourceConfig):
    """HTTP(S) download strategy filter config."""

    downloadUrl: AnyHttpUrl = Field(  # type: ignore[assignment]
        ..., description="The HTTP(S) URL, which will be downloaded."
    )
    configuration: HTTPSConfig = Field(
        HTTPSConfig(), description="HTTP(S) download strategy-specific configuration."
    )


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

    download_config: HTTPSResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateHTTPS:
        """Download via http/https and store on local cache."""
        cache = DataCache(self.download_config.configuration.datacache_config)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            req = requests.get(
                self.download_config.downloadUrl,
                allow_redirects=True,
                timeout=(3, 27),  # timeout: (connect, read) in seconds
            )
            key = cache.add(req.content)

        return SessionUpdateHTTPS(key=key)
