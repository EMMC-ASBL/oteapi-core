"""Demo-mapping strategy"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.models.mappingconfig import MappingConfig
from oteapi.plugins.factories import StrategyFactory


@dataclass
@StrategyFactory.register(("mappingType", "mapping/demo"))
class DemoMapping:
    """Mapping Interface"""

    mapping_config: MappingConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize mapping"""

        # TODO: Add initializing actions

        return {}

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Manage mapping and return shared map"""

        # TODO: Add mapping actions

        return {}
