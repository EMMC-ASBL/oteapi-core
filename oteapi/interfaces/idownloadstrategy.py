"""
Download Strategy Interface
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.resourceconfig import ResourceConfig


@dataclass
class IDownloadStrategy(Protocol):  # pylint: disable=R0903
    """Data Storage Interfaces"""

    resource_config: ResourceConfig

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dowload data from source"""

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dowload data from source"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize"""
