"""
Download Strategy Interface
"""
from dataclasses import dataclass
from typing import Protocol, Dict, Optional
from app.models.resourceconfig import ResourceConfig

@dataclass
class IDownloadStrategy(Protocol): # pylint: disable=R0903
    """ Data Storage Interfaces"""

    resource_config: ResourceConfig

    def read(self, session_id: Optional[str] = None) -> Dict:
        """ Dowload data from source """
