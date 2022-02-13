"""Strategy class for text/csv."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import ResourceConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


@dataclass
class CSVParseStrategy:
    """Parse strategy for CSV files.

    **Registers strategies**:

    - `("mediaType", "text/csv")`

    """

    parse_config: ResourceConfig

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Parse CSV."""
        print("CSV in action!")
        return {}

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}
