"""Strategy class for application/vnd.postgresql"""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlparse

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

    port: Optional[int] = Field(None, description="postgres server port number")
    host: Optional[str] = Field(None, description="postgres server hostname")
    user: Optional[str] = Field(None, description="postgres server username")
    dbname: Optional[str] = Field(None, description="postgres dbname name")
    password: Optional[str] = Field(None, description="postgres password")


class PostgresResourceConfig(ResourceConfig):
    """Postgres resource strategy resource config."""

    accessUrl: HostlessAnyUrl = Field(
        ...,
        description=ResourceConfig.__fields__["accessUrl"].field_info.description,
    )

    # TODO: what does the access Service do exactly?
    accessService: Optional[str] = Field(..., description="services to use for access?")

    sqlquery: Optional[str] = Field("", description="A SQL query string.")

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )

    connection_configuration: Optional[PostgresConnectionConfig] = Field(
        ...,
        description="Configuration for connection. Values in the accessURL take precedence.",
    )


def create_connection(resource_config: PostgresResourceConfig) -> psycopg.Connection:
    """Create a dbname connection to Postgres dbname.

    Parameters:
        psycopg_config: A dictionary providing everything needed for a psycopg
                     connection configuration

    Raises:
        psycopg.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    urlparse_result = urlparse(resource_config.accessUrl)
    user = urlparse_result.username
    password = urlparse_result.password
    dbname = urlparse_result.path[1:]
    host = urlparse_result.hostname
    port = urlparse_result.port
    if resource_config.connection_configuration is not None:
        connection_config = resource_config.connection_configuration
        if user is None:
            user = connection_config.user
        if password is None:
            password = connection_config.password
        if dbname is None:
            dbname = connection_config.dbname
        if host is None:
            host = connection_config.host
        if port is None:
            port = connection_config.port
    psycopg_config = {
        "user": user,
        "password": password,
        "dbname": dbname,
        "host": host,
        "port": port,
    }
    for key in psycopg_config:
        if psycopg_config[key] is None:
            raise AttributeError(
                "No value provided for {} in either URL or Connection Config!".format(
                    key
                )
            )

    try:
        return psycopg.connect(**psycopg_config)
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
    SQL query on the dbname to return all relevant rows.

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

        connection = create_connection(self.resource_config)
        cursor = connection.cursor()
        result = cursor.execute(self.resource_config.sqlquery).fetchall()
        connection.close()
        return SessionUpdatePostgresResource(result=result)

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "sqlquery" in session and not self.resource_config.sqlquery:
            # Use SQL query available in session
            self.resource_config.sqlquery = session["sqlquery"]
