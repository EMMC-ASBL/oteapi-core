"""Download strategy class for http/https"""

from __future__ import annotations

import sys
import warnings
from typing import Any, Optional, Union

if sys.version_info >= (3, 9, 1):
    from typing import Literal
else:
    from typing_extensions import Literal  # type: ignore[assignment]

import requests
from pydantic import AnyHttpUrl, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig


class HTTPSConfig(AttrDict):
    """HTTP(S)-specific Configuration Data Model."""

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )

    http_method: Literal["GET", "POST"] = Field(
        "GET",
        description=(
            "HTTP method to use for the download request. Only GET and POST are "
            "supported."
        ),
    )

    headers: Optional[dict[str, str]] = Field(
        None,
        description="HTTP headers to be included in the download request.",
    )

    cookies: Optional[dict[str, str]] = Field(
        None,
        description="Cookies to be included in the download request.",
    )

    query_parameters: Optional[dict[str, Union[str, list[str]]]] = Field(
        None,
        description=(
            "Query parameters to be included in the download request. Note, these can "
            "be included directly in the `downloadURL` as well."
        ),
    )

    post_body: Optional[Union[dict[str, Any], list[tuple[str, Any]], bytes]] = Field(
        None,
        description=(
            "The body of the POST request. This can be a a dictionary, list of tuples "
            "or bytes. This field is mutually exclusive with `post_body_json`."
        ),
    )

    post_body_json: Optional[Any] = Field(
        None,
        description=(
            "The body of the POST request as a JSON serializable Python object. This "
            "will be serialized to JSON and sent as the body of the POST request. "
            "This field is mutually exclusive with `post_body`."
        ),
    )

    @field_validator("http_method", mode="before")
    @classmethod
    def _upper_case_http_method(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode="after")
    def _validate_post_bodies(self) -> HTTPSConfig:
        if self.http_method == "GET" and (self.post_body or self.post_body_json):
            warnings.warn(
                "POST body is provided for a GET requests - it will be ignored.",
                stacklevel=2,
            )
            self.post_body = None
            self.post_body_json = None
        if self.post_body and self.post_body_json:
            raise ValueError(
                "Only one of post_body and post_body_json can be provided."
            )
        return self


class HTTPSResourceConfig(ResourceConfig):
    """HTTP(S) download strategy filter config."""

    downloadUrl: AnyHttpUrl = Field(  # type: ignore[assignment]
        ..., description="The HTTP(S) URL, which will be downloaded."
    )
    configuration: HTTPSConfig = Field(
        HTTPSConfig(), description="HTTP(S) download strategy-specific configuration."
    )


class HTTPDownloadContent(AttrDict):
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

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> HTTPDownloadContent:
        """Download via http/https and store on local cache."""
        cache = DataCache(self.download_config.configuration.datacache_config)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            req = requests.request(
                method=self.download_config.configuration.http_method,
                url=str(self.download_config.downloadUrl),
                allow_redirects=True,
                timeout=(3, 27),  # timeout: (connect, read) in seconds
                headers=self.download_config.configuration.headers,
                cookies=self.download_config.configuration.cookies,
                params=self.download_config.configuration.query_parameters,
                # No reason to check the method is correct for sending content (POST),
                # since this is validated in the config model.
                data=self.download_config.configuration.post_body,
                json=self.download_config.configuration.post_body_json,
            )
            key = cache.add(req.content)

        return HTTPDownloadContent(key=key)
