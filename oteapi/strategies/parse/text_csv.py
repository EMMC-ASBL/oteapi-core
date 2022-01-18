"""Strategy class for text/csv."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(("mediaType", "text/csv"))
class CSVParseStrategy:

    resource_config: "ResourceConfig"

    def parse(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        print("CSV in action!")
        return {}

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize"""
        return {}
