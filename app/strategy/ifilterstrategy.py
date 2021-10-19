"""
Resource Strategy Interface
"""

from typing import Protocol, Dict, Optional
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig

@dataclass
class IFilterStrategy(Protocol):
    """ Resource Interface """

    filter_config : FilterConfig

    def get(self, session_id: Optional[str] = None) -> Dict:
        """ Execute strategy and return a dictionary """
