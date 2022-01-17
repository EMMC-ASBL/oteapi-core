"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.resourceconfig import ResourceConfig


@dataclass
class IResourceStrategy(Protocol):  # pylint: disable=R0903
    """Resource  Interfaces"""

    resource_config: ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Run get-method and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
