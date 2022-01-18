"""Strategy class for text/json."""
# pylint: disable=unused-argument
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.datacache.datacache import DataCache
from oteapi.models.resourceconfig import ResourceConfig
from oteapi.plugins.factories import StrategyFactory, create_download_strategy


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONDataParseStrategy:

    resource_config: ResourceConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize"""
        return {}

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse json."""
        downloader = create_download_strategy(self.resource_config)
        output = downloader.get()
        cache = DataCache(self.resource_config.configuration)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return content
        return json.loads(content)
