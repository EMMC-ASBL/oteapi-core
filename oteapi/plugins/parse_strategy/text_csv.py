""" Strategy class for text/csv """

from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategy-interfaces.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("mediaType", "text/csv"))
class CSVParseStrategy:

    resource_config: ResourceConfig

    def parse(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        print("CSV in action!")
        return {}

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return dict()
