"""Strategy class for text/csv."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.models.resourceconfig import ResourceConfig
from oteapi.plugins.factories import StrategyFactory


@dataclass
@StrategyFactory.register(("mediaType", "text/csv"))
class CSVParseStrategy:

    resource_config: ResourceConfig

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        print("CSV in action!")
        return {}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize"""
        return {}
