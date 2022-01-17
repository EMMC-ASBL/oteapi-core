"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.resourceconfig import ResourceConfig


@dataclass
class IParseStrategy(Protocol):  # pylint: disable=R0903
    """Data Storage Interfaces"""

    resource_config: ResourceConfig

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """run parser and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
