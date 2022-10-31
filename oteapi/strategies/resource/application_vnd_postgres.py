"""Strategy class for application/vnd.postgresql"""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Optional

import psycopg
from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.models.resourceconfig import HostlessAnyUrl

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class PostgresConnectionConfig(AttrDict):
    """Configuration data model for
    [`PostgresResourceStrategy`][oteapi.strategies.resource.application_vnd_postgres.PostgresParseStrategy]."""

    connection_dict: dict = Field(
        ..., description="Dictionary used for connection with postgres DB via psycopg."
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )

    # TODO seems a bit strange to have the sqlquery here, artifact from
    #     importing from the sqllite version
    sqlquery: Optional[str] = Field("", description="A SQL query string.")


class PostgresResourceConfig(ResourceConfig):
    """Postgres resource strategy resource config."""

    # TODO: accessUrl and accessService are required, but in this implmentation do nothing, discuss!
    accessUrl: HostlessAnyUrl = Field(
        ...,
        description=ResourceConfig.__fields__["accessUrl"].field_info.description,
    )
    accessService: Optional[str] = Field(..., description="services to use for access?")

    configuration: PostgresConnectionConfig = Field(
        ...,
        description="Postgres resource strategy-specific configuration.",
    )


def create_connection(conn_config: dict) -> psycopg.Connection:
    """Create a database connection to Postgres database.

    Parameters:
        conn_config: A dictionary providing everything needed for a psycopg
                     connection configuration

    Raises:
        psycopg.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    try:
        return psycopg.connect(**conn_config)
    except psycopg.Error as exc:
        raise psycopg.Error("Could not connect to given Postgres DB.") from exc


class SessionUpdatePostgresResource(SessionUpdate):
    """Configuration model for PostgresResource."""

    result: list = Field(..., description="List of results from the query.")


@dataclass
class PostgresResourceStrategy:
    """Resource strategy for Postgres.

    **Registers strategies**:

    #TODO: replace with the 'correct' information
    - `("mediaType", "application/vnd.postgres")`

    Purpose of this strategy: Connect to a postgres DB and run a
    SQL query on the database to return all relevant rows.

    """

    resource_config: PostgresResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        return SessionUpdate()

    def get(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdatePostgresResource:
        """Resource Postgres query responses."""
        if session:
            self._use_filters(session)
        session = session if session else {}

        conn_config = self.resource_config.configuration.connection_dict

        connection = create_connection(conn_config)
        cursor = connection.cursor()
        result = cursor.execute(self.resource_config.configuration.sqlquery).fetchall()
        connection.close()
        return SessionUpdatePostgresResource(result=result)

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "sqlquery" in session and not self.resource_config.configuration.sqlquery:
            # Use SQL query available in session
            self.resource_config.configuration.sqlquery = session["sqlquery"]
