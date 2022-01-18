"""Download Strategy Interface"""
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.resourceconfig import ResourceConfig


@dataclass  # type: ignore[misc]
class IDownloadStrategy(Protocol):
    """Download Interfaces"""

    resource_config: ResourceConfig

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dowload data from source"""

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dowload data from source"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize"""
