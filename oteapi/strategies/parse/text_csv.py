"""Strategy class for text/csv."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(("mediaType", "text/csv"))
class CSVParseStrategy:
    """Parse strategy for CSV files.

    **Registers strategies**:

    - `("mediaType", "text/csv")`

    """

    resource_config: "ResourceConfig"

    def parse(self, **_) -> "Dict[str, Any]":
        """Parse CSV."""
        print("CSV in action!")
        return {}

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize."""
        return {}
