# pylint: disable=W0613, W0511
"""Download strategy class for file"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(
    ("scheme", "file"),
)
class FileStrategy:
    """Strategy for retrieving data via local file."""

    resource_config: ResourceConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Read local file."""
        # pylint: disable=E1101
        assert self.resource_config.downloadUrl
        assert self.resource_config.downloadUrl.scheme == "file"
        filename = self.resource_config.downloadUrl.host
        return dict(filename=filename)
