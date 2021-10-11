"""
Data Storage Interface
"""

from dataclasses import dataclass
from typing import Protocol, Dict, Optional
from app.models.resourceconfig import ResourceConfig

@dataclass
class IParseStrategy(Protocol): # pylint: disable=R0903
    """ Data Storage Interfaces"""

    resource_config : ResourceConfig

    def parse(self, session_id: Optional[str] = None) -> Dict:
        """ run parser and return a dictionary """
