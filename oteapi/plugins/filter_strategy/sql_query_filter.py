# pylint: disable=W0511, W0613
"""
SQL query filter strategy
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.models.filterconfig import FilterConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from pydantic import BaseModel


class SqlQueryDataModel(BaseModel):
    query: str


@dataclass
@StrategyFactory.register(("filterType", "filter/sql"))
class QFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""
        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Missing session",
            )
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        retobj = dict(sqlquery=queryData.query)

        return retobj

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""
        return dict()
