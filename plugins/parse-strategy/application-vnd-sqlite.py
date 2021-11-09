""" Strategy class for application/vnd.sqlite3 """

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(
    ("mediaType", "application/vnd.sqlite3"),
    ("mediaType", "application/vnd.sqlite"),
    ("mediaType", "application/sqlite")
)
class SqliteParseStrategy:

    resource_config: ResourceConfig

    def parse(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        print("Sqlite in action!")
        return {}

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return dict()

