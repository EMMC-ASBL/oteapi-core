"""
Resource Strategy Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.filterconfig import FilterConfig


@dataclass
class IFilterStrategy(Protocol):
    """Resource Interface"""

    filter_config: FilterConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute strategy and return a dictionary"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize strategy and return a dictionary"""
