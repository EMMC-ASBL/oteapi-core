"""Strategy class for text/csv."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from oteapi.models.sessionupdate import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


class SessionUpdateCSVParse(SessionUpdate):
    """Class for returning values from CSVParse."""

    # returns nothing...


@dataclass
class CSVParseStrategy:
    """Parse strategy for CSV files.

    **Registers strategies**:

    - `("mediaType", "text/csv")`

    """

    parse_config: "ResourceConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateCSVParse:
        """Parse CSV."""
        print("CSV in action!")
        return SessionUpdateCSVParse()

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()
