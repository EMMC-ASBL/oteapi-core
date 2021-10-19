"""
Resource Strategy Interface
"""

from typing import Protocol, Dict, Optional, Any
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig

@dataclass
class IFilterStrategy(Protocol):
    """ Resource Interface """

    filter_config : FilterConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Execute strategy and return a dictionary """
