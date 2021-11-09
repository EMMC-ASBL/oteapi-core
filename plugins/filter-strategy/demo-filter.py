# pylint: disable=W0511, W0613
"""
Demo-filter strategy
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("filterType", "filter/demo"))
class DemoFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""

        # TODO: Add logic
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""

        # TODO: Add logic
        print("I GOT A SESSION!", session)
        return dict(foo="bar")
