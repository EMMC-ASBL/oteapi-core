# pylint: disable=W0511, W0613
"""
Demo-mapping strategy
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory
from app.strategy.idownloadstrategy import create_download_strategy


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
