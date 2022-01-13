"""
Download Strategy Interface
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.app.models.resourceconfig import ResourceConfig
from oteapi.app.strategy.factory import StrategyFactory


@dataclass
class IDownloadStrategy(Protocol):  # pylint: disable=R0903
    """Data Storage Interfaces"""

    resource_config: ResourceConfig

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Dowload data from source"""

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Dowload data from source"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""


def create_download_strategy(resource_config: ResourceConfig) -> IDownloadStrategy:
    """Helper function to simplify creating a download strategy"""
    return StrategyFactory.make_strategy(
        resource_config, index=("scheme", resource_config.downloadUrl.scheme)
    )
