# pylint: disable=W0511, W0613
"""
Demo-mapping strategy
"""
from typing import Dict, Optional
from dataclasses import dataclass
from app.models.resourceconfig import ResourceConfig
from app.strategy import factory


@dataclass
class DemoResource:
    """ Mapping Interface """

    resource_config : ResourceConfig

    def get(self, session_id: Optional[str] = None) -> Dict:
        """ Manage mapping and return shared map """

        # TODO: Add mapping actions

        return dict()


def initialize() -> None:
    factory.register_resource_strategy("resource/demo", DemoResource)
