"""Strategy class for application/vnd.sqlite3."""
# pylint: disable=unused-argument
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class SqliteParseConfig(AttrDict):
    """Configuration data model for
    [`SqliteParseStrategy`][oteapi.strategies.parse.application_vnd_sqlite.SqliteParseStrategy].
    """

    sqlquery: str = Field("", description="A SQL query string.")
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )


class SqliteParserResourceConfig(ResourceConfig):
    """SQLite parse strategy resource config."""

    mediaType: str = Field(
        "application/vnd.sqlite3",
        const=True,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: SqliteParseConfig = Field(
        SqliteParseConfig(), description="SQLite parse strategy-specific configuration."
    )


def create_connection(db_file: Path) -> sqlite3.Connection:
    """Create a database connection to SQLite database.

    Parameters:
        db_file: Full path to SQLite database file.

    Raises:
        sqlite3.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as exc:
        raise sqlite3.Error("Could not connect to given SQLite DB.") from exc


class SessionUpdateSqLiteParse(SessionUpdate):
    """Configuration model for SqLiteParse."""

    result: list = Field(..., description="List of results from the query.")


@dataclass
class SqliteParseStrategy:
    """Parse strategy for SQLite.

    **Registers strategies**:

    - `("mediaType", "application/vnd.sqlite3")`

    Purpose of this strategy: Download a SQLite database using `downloadUrl` and run a
    SQL query on the database to return all relevant rows.

    """

    parse_config: SqliteParserResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        return SessionUpdate()

    def get(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdateSqLiteParse:
        """Parse SQLite query responses."""
        if session:
            self._use_filters(session)
        session = session if session else {}

        # Retrieve SQLite file
        download_config = self.parse_config.copy()
        del download_config.configuration
        downloader = create_strategy("download", download_config)
        session.update(downloader.initialize(session))
        cache_key = downloader.get(session).get("key", "")

        cache = DataCache(self.parse_config.configuration.datacache_config)
        with cache.getfile(cache_key, suffix="db") as filename:
            connection = create_connection(filename)
            cursor = connection.cursor()
            result = cursor.execute(self.parse_config.configuration.sqlquery).fetchall()
            connection.close()
        return SessionUpdateSqLiteParse(result=result)

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "sqlquery" in session and not self.parse_config.configuration.sqlquery:
            # Use SQL query available in session
            self.parse_config.configuration.sqlquery = session["sqlquery"]
