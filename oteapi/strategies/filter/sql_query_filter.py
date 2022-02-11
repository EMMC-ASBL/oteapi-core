"""SQL query filter strategy."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import Field

from oteapi.models.sessionupdate import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import FilterConfig


class SessionUpdateSqlQuery(SessionUpdate):
    """Class for returning values from SQL Query data model."""

    query: str = Field(..., description="A SQL query string.")


@dataclass
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: "FilterConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdateSqlQuery:
        """Initialize strategy and return a dictionary"""
        queryData = SessionUpdateSqlQuery(**{"query": self.filter_config.query})
        return queryData

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute strategy and return a dictionary"""
        return SessionUpdate()
