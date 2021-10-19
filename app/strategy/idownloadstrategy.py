"""
Download Strategy Interface
"""
from dataclasses import dataclass
from typing import Protocol, Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig

@dataclass
class IDownloadStrategy(Protocol): # pylint: disable=R0903
    """ Data Storage Interfaces"""

    resource_config: ResourceConfig

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Dowload data from source """
