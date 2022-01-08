""" Strategy class for text/json """
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.cache.cache import DataCache
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory
from app.strategy.idownloadstrategy import create_download_strategy


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONDataParseStrategy:

    resource_config: ResourceConfig

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return dict()

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
