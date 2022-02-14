"""Strategy class for application/json."""
# pylint: disable=unused-argument
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import Field

from oteapi.datacache import DataCache
from oteapi.models.sessionupdate import SessionUpdate
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


class SessionUpdateJSONParse(SessionUpdate):
    """Class for returning values from JSON Parse."""

    content: dict = Field(..., description="Content of the JSON document.")


@dataclass
class JSONDataParseStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("mediaType", "application/json")`

    """

    parse_config: "ResourceConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateJSONParse:
        """Parse json."""
        downloader = create_strategy("download", self.parse_config)
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return SessionUpdateJSONParse(content=content)
        return SessionUpdateJSONParse(content=json.loads(content))
