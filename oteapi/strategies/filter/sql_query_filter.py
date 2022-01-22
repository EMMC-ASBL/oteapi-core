"""SQL query filter strategy"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import FilterConfig


class SqlQueryDataModel(BaseModel):
    """SQL Query data model."""

    query: str = Field(..., description="A SQL query string.")


@dataclass
@StrategyFactory.register(("filterType", "filter/sql"))
class SQLQueryFilter:
    """Strategy for a SQL query filter.

    **Registers strategies**:

    - `("filterType", "filter/sql")`

    """

    filter_config: "FilterConfig"

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary"""
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        return {"sqlquery": queryData.query}

    def get(self, **_) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""
        return {}
