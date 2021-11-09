""" Strategy class for text/json """

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONDataParseStrategy:

    resource_config: ResourceConfig

    def parse(
        self, session: Optional[Dict[str, Any]] = None
    ) -> Dict:  # pylint: disable=W0613
        print("JSON in action!")
        return {}

    def initialize(
        self, session: Optional[Dict[str, Any]] = None
    ) -> Dict:  # pylint: disable=W0613
        """Initialize"""
        return dict()
