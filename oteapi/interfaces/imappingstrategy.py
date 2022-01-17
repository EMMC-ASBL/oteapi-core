"""
Mapping Strategy Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.mappingconfig import MappingConfig


@dataclass
class IMappingStrategy(Protocol):
    """Mapping Interface"""

    mapping_config: MappingConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""
