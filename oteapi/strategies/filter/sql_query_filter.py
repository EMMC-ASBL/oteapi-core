"""SQL query filter strategy"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel

from oteapi.models.filterconfig import FilterConfig
from oteapi.plugins.factories import StrategyFactory


class SqlQueryDataModel(BaseModel):
    query: str


@dataclass
@StrategyFactory.register(("filterType", "filter/sql"))
class QFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize strategy and return a dictionary"""
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        return {"sqlquery": queryData.query}

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute strategy and return a dictionary"""
        return {}
