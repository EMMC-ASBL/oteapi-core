"""Strategy class for application/vnd.postgresql"""
# pylint: disable=unused-argument
import psycopg
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


# NOTE: common to all SQL configs
class PostgresParseConfig(AttrDict):
    """Configuration data model for
    [`PostgresParseStrategy`][oteapi.strategies.parse.application_vnd_postgres.PostgresParseStrategy]."""

    sqlquery: str = Field("", description="A SQL query string.")
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )


class PostgresParserResourceConfig(ResourceConfig):
    """Postgres parse strategy resource config."""

    mediaType: str = Field(
        "application/vnd.postgres",
        const=True,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: PostgresParseConfig = Field(
        PostgresParseConfig(), description="Postgres parse strategy-specific configuration."
    )


def create_connection(conn_config: dict) -> psycopg.Connection:
    """Create a database connection to Postgres database.

    Parameters:
        pos: Full path to Postgres database file.

    Raises:
        psycopg.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    try:
        return psycopg.connect(**conn_config)
    except psycopg.Error as exc:
        raise psycopg.Error("Could not connect to given Postgres DB.") from exc


class SessionUpdatePostgresParse(SessionUpdate):
    """Configuration model for PostgresParse."""

    result: list = Field(..., description="List of results from the query.")


@dataclass
class PostgresParseStrategy:
    """Parse strategy for Postgres.

    **Registers strategies**:

    - `("mediaType", "application/vnd.postgres")`

    Purpose of this strategy: Connect to a postgres DB and run a
    SQL query on the database to return all relevant rows.

    """

    parse_config: PostgresParserResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        return SessionUpdate()

    def get(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdatePostgresParse:
        """Parse Postgres query responses."""
        if session:
            self._use_filters(session)
        session = session if session else {}

        # Not yet sure how to set up the connection config...
        conn_config = self.parse_config.copy()['conn_config']

        connection = create_connection(conn_config)
        cursor = connection.cursor()
        result = cursor.execute(self.parse_config.configuration.sqlquery).fetchall()
        connection.close()
        return SessionUpdatePostgresParse(result=result)

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "sqlquery" in session and not self.parse_config.configuration.sqlquery:
            # Use SQL query available in session
            self.parse_config.configuration.sqlquery = session["sqlquery"]
