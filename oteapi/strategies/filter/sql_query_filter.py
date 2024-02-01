"""SQL query filter strategy."""
from typing import TYPE_CHECKING, Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig

if TYPE_CHECKING:  # pragma: no cover
    pass


class SqlQueryFilterConfig(FilterConfig):
    """SQL query filter strategy filter config."""

    filterType: Literal["filter/sql"] = Field(
        "filter/sql",
        description=FilterConfig.model_fields["filterType"].description,
    )
    query: str = Field(..., description="A SQL query string.")


class AttrDictSqlQuery(AttrDict):
    """Class for returning values from SQL Query data model."""

    sqlquery: str = Field(..., description="A SQL query string.")


@dataclass
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: SqlQueryFilterConfig

    def initialize(self) -> AttrDictSqlQuery:
        """Initialize strategy."""
        return AttrDictSqlQuery(sqlquery=self.filter_config.query)

    def get(self) -> AttrDict:
        """Execute strategy and return a dictionary."""
        return AttrDict()
