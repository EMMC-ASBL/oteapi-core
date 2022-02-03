"""Strategy class for application/vnd.sqlite3."""
# pylint: disable=unused-argument
import sqlite3
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as exc:
        print(exc)

    return conn


@dataclass
class SqliteParseStrategy:
    """Parse strategy for SQLite.

    **Registers strategies**:

    - `("mediaType", "application/vnd.sqlite3")`

    """

    parse_config: "ResourceConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Parse SQLite query responses."""
        if session is None:
            raise ValueError("Missing session")

        if "sqlquery" in session:
            cn = create_connection(session["filename"])
            cur = cn.cursor()
            rows = cur.execute(session["sqlquery"]).fetchall()
            return {"result": rows}
        return {"result": "No query given"}

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}
