"""Strategy class for application/json."""
# pylint: disable=unused-argument
import json
from typing import TYPE_CHECKING, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class JSONConfig(AttrDict):
    """JSON parse-specific Configuration Data Model."""

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configurations for the data cache for storing the downloaded file content.",
    )


class JSONResourceConfig(ResourceConfig):
    """JSON parse strategy filter config."""

    mediaType: str = Field(
        "application/json",
        const=True,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: JSONConfig = Field(
        JSONConfig(), description="JSON parse strategy-specific configuration."
    )


class SessionUpdateJSONParse(SessionUpdate):
    """Class for returning values from JSON Parse."""

    content: dict = Field(..., description="Content of the JSON document.")


@dataclass
class JSONDataParseStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("mediaType", "application/json")`

    """

    parse_config: JSONResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateJSONParse:
        """Parse json."""
        downloader = create_strategy("download", self.parse_config)
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration.datacache_config)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return SessionUpdateJSONParse(content=content)
        return SessionUpdateJSONParse(content=json.loads(content))
