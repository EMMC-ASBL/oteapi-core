"""SQL query filter strategy"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import BaseModel

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import FilterConfig


class SqlQueryDataModel(BaseModel):
    query: str


@dataclass
@StrategyFactory.register(("filterType", "filter/sql"))
class SQLQueryFilter:

    filter_config: "FilterConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary"""
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        return {"sqlquery": queryData.query}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""
        return {}
