# pylint: disable=W0511, W0613
"""
Demo-filter strategy
"""
from typing import Dict, Optional
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy import factory

@dataclass
class DemoFilter:

    filter_config : FilterConfig

    def get(self, session_id: Optional[str] = None) -> Dict:
        """ Execute strategy and return a dictionary """

        # TODO: Add logic

        return dict()

def initialize() -> None:
    factory.register_filter_strategy("filter/demo", DemoFilter)