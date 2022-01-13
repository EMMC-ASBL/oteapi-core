"""
Mapping Strategy Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.app.models.mappingconfig import MappingConfig
from oteapi.app.strategy.factory import StrategyFactory


@dataclass
class IMappingStrategy(Protocol):
    """Mapping Interface"""

    mapping_config: MappingConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""


def create_mapping_strategy(mapping_config: MappingConfig) -> IMappingStrategy:
    """Helper function to simplify creating a filter strategy"""
    return StrategyFactory.make_strategy(mapping_config, "mappingType")
