""" Strategy class for text/json """
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.datacache.datacache import DataCache
from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from oteapi.strategy-interfaces.idownloadstrategy import create_download_strategy


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONDataParseStrategy:

    resource_config: ResourceConfig

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return {}

    def parse(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Parse json."""
        downloader = create_download_strategy(self.resource_config)
        output = downloader.get()
        cache = DataCache(self.resource_config.configuration)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return content
        else:
            return json.loads(content)
