# pylint: disable=W0511, W0613
"""
Demo-mapping strategy
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from oteapi.strategy-interfaces.idownloadstrategy import create_download_strategy


@dataclass
@StrategyFactory.register(("accessService", "demo-access-service"))
class DemoResource:
    """Mapping Interface"""

    resource_config: ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Manage mapping and return shared map"""

        # Example of the plugin using the download strategy to fetch the data
        download_strategy = create_download_strategy(self.resource_config)
        read_output = download_strategy.read({})
        print(read_output)
        return dict()

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()
