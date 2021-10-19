""" Strategy class for text/json """

from dataclasses import dataclass
from app.strategy import factory
from typing import Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig

@dataclass
class JSONDataParseStrategy:

    resource_config: ResourceConfig

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict: #pylint: disable=W0613
        print ("JSON in action!")
        return {}

def initialize() -> None:
    factory.register_parse_strategy("text/json", JSONDataParseStrategy)
