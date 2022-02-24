"""Strategy class for text/csv."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import ResourceConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


@dataclass
class CSVParseStrategy:
    """Parse strategy for CSV files.

    **Registers strategies**:

    - `("mediaType", "text/csv")`

    Note: This strategy is currently not finished, and is therefore not registered.

    """

    parse_config: ResourceConfig

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Parse CSV."""
        return SessionUpdate()

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()
