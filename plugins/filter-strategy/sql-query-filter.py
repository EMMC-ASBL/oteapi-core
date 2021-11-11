# pylint: disable=W0511, W0613
"""
SQL query filter strategy
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from fastapi import HTTPException

from pydantic import BaseModel

from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory


class SqlQueryDataModel(BaseModel):
    query: str


@dataclass
@StrategyFactory.register(("filterType", "filter/sql"))
class QFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""
        print("in initalize")
        if (session == None):
            raise HTTPException(
                status_code=404,
                detail="Missing session",)
        print("in get")
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        retobj = dict(sqlquery=queryData.query)

        return retobj
        # TODO: Add logic
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""

        if (session == None):
            raise HTTPException(
                status_code=404,
                detail="Missing session",)
        print("in get")
        queryData = SqlQueryDataModel(**{"query": self.filter_config.query})
        retobj = dict(sqlquery=queryData.query)

        return retobj

