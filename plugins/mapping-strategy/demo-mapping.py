# pylint: disable=W0511, W0613
"""
Demo-mapping strategy
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.mappingconfig import MappingConfig
from app.strategy import factory


@dataclass
class DemoMapping:
    """ Mapping Interface """

    mapping_config: MappingConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Manage mapping and return shared map """

        # TODO: Add mapping actions

        return {}


def initialize() -> None:
    factory.register_mapping_strategy("mapping/demo", DemoMapping)
