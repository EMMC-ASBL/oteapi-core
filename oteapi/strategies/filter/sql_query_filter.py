"""SQL query filter strategy."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig


class SqlQueryFilterConfig(FilterConfig):
    """SQL query filter strategy filter config."""

    filterType: Literal["filter/sql"] = Field(
        "filter/sql",
        description=FilterConfig.model_fields["filterType"].description,
    )
    query: str = Field(..., description="A SQL query string.")


class SqlQueryContent(AttrDict):
    """Class for returning values from SQL Query data model."""

    sqlquery: str = Field(..., description="A SQL query string.")


@dataclass
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: SqlQueryFilterConfig

    def initialize(self) -> SqlQueryContent:
        """Initialize strategy."""
        return SqlQueryContent(sqlquery=self.filter_config.query)

    def get(self) -> AttrDict:
        """Execute strategy and return a dictionary."""
        return AttrDict()
