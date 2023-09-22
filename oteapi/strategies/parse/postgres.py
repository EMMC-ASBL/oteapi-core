"""Strategy class for application/vnd.postgresql"""
from typing import Any, Dict, Optional
from urllib.parse import urlunparse

import psycopg

from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.utils._pydantic import AnyUrl, Field
from oteapi.utils._pydantic import dataclasses as pydantic_dataclasses
from oteapi.utils._pydantic import parse_obj_as, root_validator


class PostgresConfig(AttrDict):
    """Configuration data model for
    [`PostgresResourceStrategy`][oteapi.strategies.parse.postgres.PostgresResourceConfig].
    """

    user: Optional[str] = Field(None, description="postgres server username")
    dbname: Optional[str] = Field(None, description="postgres dbname name")
    password: Optional[str] = Field(None, description="postgres password")

    sqlquery: Optional[str] = Field("", description="A SQL query string.")


class PostgresResourceConfig(ResourceConfig):
    """Postgresql parse strategy config"""

    configuration: PostgresConfig = Field(
        PostgresConfig(),
        description=(
            "Configuration for resource. " "Values in the accessURL take precedence."
        ),
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )

    @classmethod
    def _urlconstruct(
        cls,  # PEP8 - Always use cls for the first argument to class methods.
        scheme: Optional[str] = "",  # Schema defining link format
        user: Optional[str] = None,  # Username
        password: Optional[str] = None,  # Password
        host: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = "",
        params: Optional[str] = "",
        query: Optional[str] = "",
        fragment: Optional[str] = "",
    ):
        """Construct a pydantic AnyUrl based on the given URL properties"""

        # Hostname should always be given
        if not host:
            raise ValueError("hostname must be specified")

        # Update netloc of username or username|password pair is defined
        netloc = host
        if user and not password:  # Only username is provided. OK
            netloc = f"{user}@{host}"
        elif user and password:  # Username and password is provided. OK
            netloc = f"{user}:{password}@{host}"
        else:  # Password and no username is provided. ERROR
            raise ValueError("username not provided")

        # Append port if port is defined
        netloc = netloc if not port else f"{netloc}:{port}"

        # Construct a URL from a tuple of URL-properties
        unparsed = urlunparse([scheme, netloc, path, params, query, fragment])

        # Populate and return a Pydantic URL
        return parse_obj_as(AnyUrl, unparsed)

    @root_validator
    def adjust_url(cls, values):
        """Root Validator
        Verifies configuration consistency, merge configurations
        and update the accessUrl property.
        """

        # Copy model-state into placeholders
        config = values.get("configuration")
        accessUrl = values["accessUrl"]

        # Check and merge user configuration
        user = accessUrl.user if accessUrl.user else config["user"]
        if config["user"] and user != config["user"]:
            raise ValueError("mismatching username in accessUrl and configuration")

        # Check and merge password configuration
        password = accessUrl.password if accessUrl.password else config["password"]
        if config["password"] and password != config["password"]:
            raise ValueError("mismatching password in accessUrl and configuration")

        # Check and merge database name configuration
        dbname = accessUrl.path if accessUrl.path else config["dbname"]
        if config["dbname"] and dbname != config["dbname"]:
            raise ValueError("mismatching dbname in accessUrl and configuration")

        # Reconstruct accessUrl from the updated properties
        values["accessUrl"] = cls._urlconstruct(
            scheme=accessUrl.scheme,
            host=accessUrl.host,
            port=accessUrl.port,
            user=user,
            password=password,
        )
        return values


def create_connection(resource_config: PostgresResourceConfig) -> psycopg.Connection:
    """Create a dbname connection to Postgres dbname.

    Parameters:
        resource_config: A dictionary providing everything needed for a psycopg
                     connection configuration

    Raises:
        psycopg.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    try:
        return psycopg.connect(resource_config.accessUrl)
    except psycopg.Error as exc:
        raise psycopg.Error("Could not connect to given Postgres DB.") from exc


class SessionUpdatePostgresResource(SessionUpdate):
    """Configuration model for PostgresResource."""

    result: list = Field(..., description="List of results from the query.")


@pydantic_dataclasses.dataclass
class PostgresResourceStrategy:
    """Resource strategy for Postgres.

    **Registers strategies**:

    - `("accessService", "postgres")`

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
        result = cursor.execute(self.resource_config.configuration.sqlquery).fetchall()
        connection.close()
        return SessionUpdatePostgresResource(result=result)

    def _use_filters(self, session: "Dict[str, Any]") -> None:
        """Update `config` according to filter values found in the session."""
        if "sqlquery" in session and not self.resource_config.configuration.sqlquery:
            # Use SQL query available in session
            self.resource_config.configuration.sqlquery = session["sqlquery"]
