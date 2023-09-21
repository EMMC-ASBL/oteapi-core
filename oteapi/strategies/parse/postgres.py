"""Strategy class for application/vnd.postgresql"""
from typing import Any, Dict, Optional

import psycopg
from pydantic import AnyUrl, BaseModel, Field, model_validator
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate


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

    @model_validator(mode="before")
    @classmethod
    def adjust_url(cls, data: Any) -> "PostgresResourceConfig":
        """Model Validator
        Verifies configuration consistency, merge configurations
        and update the accessUrl property.
        """
        if isinstance(data, BaseModel):
            data = data.model_dump()
        elif not isinstance(data, dict):
            raise TypeError(
                "invalid data type, should be either dict or pydantic model"
            )

        if "accessUrl" not in data:
            raise ValueError("missing accessUrl in PostgreSQL resource configuration")

        accessUrl = AnyUrl(data["accessUrl"])
        default_config = PostgresConfig()

        if not accessUrl.host:
            raise ValueError("missing host in accessUrl")

        # Check and merge user configuration
        user = (
            accessUrl.username
            if accessUrl.username
            else data.get("configuration", {}).get("user", default_config.user)
        )
        if data.get("configuration", {}).get(
            "user", default_config.user
        ) and user != data.get("configuration", {}).get("user", default_config.user):
            raise ValueError("mismatching username in accessUrl and configuration")

        # Check and merge password configuration
        password = (
            accessUrl.password
            if accessUrl.password
            else data.get("configuration", {}).get("password", default_config.password)
        )
        if data.get("configuration", {}).get(
            "password", default_config.password
        ) and password != data.get("configuration", {}).get(
            "password", default_config.password
        ):
            raise ValueError("mismatching password in accessUrl and configuration")

        # Check and merge database name configuration
        dbname = (
            accessUrl.path
            if accessUrl.path
            else data.get("configuration", {}).get("dbname", default_config.dbname)
        )
        if data.get("configuration", {}).get(
            "dbname", default_config.dbname
        ) and dbname != data.get("configuration", {}).get(
            "dbname", default_config.dbname
        ):
            raise ValueError("mismatching dbname in accessUrl and configuration")

        # Reconstruct accessUrl from the updated properties
        data["accessUrl"] = accessUrl.__class__.build(
            scheme=accessUrl.scheme,
            username=user,
            password=password,
            host=accessUrl.host,
            port=accessUrl.port,
            path=dbname,
            query=accessUrl.query,
            fragment=accessUrl.fragment,
        )
        return data


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


@dataclass
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
            if not isinstance(session["sqlquery"], str):
                raise TypeError("sqlquery (found in session) must be a string")
            # Use SQL query available in session
            self.resource_config.configuration.sqlquery = session["sqlquery"]
