"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Protocol, Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig

@dataclass
class IResourceStrategy(Protocol): # pylint: disable=R0903
    """ Resource  Interfaces"""

    resource_config : ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Run get-method and return a dictionary """
