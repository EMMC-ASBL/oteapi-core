"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Protocol, Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
class IParseStrategy(Protocol):  # pylint: disable=R0903
    """Data Storage Interfaces"""

    resource_config: ResourceConfig

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """run parser and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""


def create_parse_strategy(resource_config: ResourceConfig) -> IParseStrategy:
    """Helper function to simplify creating a parse strategy"""
    return StrategyFactory.make_strategy(resource_config, field="mediaType")
