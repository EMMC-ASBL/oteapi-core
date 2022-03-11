"""SQL query filter strategy."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import FilterConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class SqlQueryFilterConfig(FilterConfig):
    """SQLite query filter strategy filter config."""

    filterType: str = Field(
        "filter/sql",
        const=True,
        description=FilterConfig.__fields__["filterType"].field_info.description,
    )
    query: str = Field(..., description="A SQL query string.")


class SessionUpdateSqlQuery(SessionUpdate):
    """Class for returning values from SQL Query data model."""

    sqlquery: str = Field(..., description="A SQL query string.")


@dataclass
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: SqlQueryFilterConfig

    def initialize(
        self,
        session: "Optional[Dict[str, Any]]" = None,
    ) -> SessionUpdateSqlQuery:
        """Initialize strategy."""
        return SessionUpdateSqlQuery(sqlquery=self.filter_config.query)

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute strategy and return a dictionary."""
        return SessionUpdate()
