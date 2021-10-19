"""
Mapping Strategy Interface
"""

from dataclasses import dataclass
from typing import Protocol, Dict, Optional, Any
from app.models.mappingconfig import MappingConfig

@dataclass
class IMappingStrategy(Protocol):
    """ Mapping Interface """

    mapping_config: MappingConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Execute strategy and return a dictionary """
