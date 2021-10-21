"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Protocol, Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory

@dataclass
class IResourceStrategy(Protocol):  # pylint: disable=R0903
    """ Resource  Interfaces"""

    resource_config: ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Run get-method and return a dictionary """

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize"""


def create_resource_strategy(resource_config: ResourceConfig) -> IResourceStrategy:
    """ Helper function to instanciate a resource strategy """
    return StrategyFactory.make_strategy(resource_config, 'accessService')
