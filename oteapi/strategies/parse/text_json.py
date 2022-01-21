"""Strategy class for text/json."""
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from oteapi.datacache import DataCache
from oteapi.plugins.factories import StrategyFactory, create_download_strategy

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONDataParseStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("mediaType", "text/json")`

    """

    resource_config: "ResourceConfig"

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def parse(self, **_) -> "Dict[str, Any]":
        """Parse json."""
        downloader = create_download_strategy(self.resource_config)
        output = downloader.get()
        cache = DataCache(self.resource_config.configuration)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return content
        return json.loads(content)
