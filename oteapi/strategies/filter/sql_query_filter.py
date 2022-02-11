"""SQL query filter strategy."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import FilterConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class SqlQueryFilterConfig(FilterConfig):
    """SQLite query filter strategy filter config."""

    query: str = Field(..., description="A SQL query string.")


@dataclass
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: SqlQueryFilterConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary"""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary."""
        return {"sqlquery": self.filter_config.query}
