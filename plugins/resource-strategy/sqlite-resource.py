# pylint: disable=W0511, W0613
"""
Demo-mapping strategy
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory
from app.strategy.idownloadstrategy import create_download_strategy
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


@dataclass
@StrategyFactory.register(("accessService", "sqlite-service"))
class SqliteResource:
    """Sqlite resouce"""

    resource_config: ResourceConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Set up an sqlite service"""

        print("hello from sqlite-plugin")
        print(self.resource_config)
        if self.resource_config.configuration:
            conf = self.resource_config.configuration
        else:
            conf = {}
        if "query" in conf:
            print("querying")
            download_strategy = create_download_strategy(self.resource_config)
            read_output = download_strategy.read({})
            cn = create_connection(read_output['filename'])
            cur = cn.cursor()
            rows = cur.execute(conf["query"]).fetchall()
        return dict(result=rows, filename=read_output['filename'])

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()

