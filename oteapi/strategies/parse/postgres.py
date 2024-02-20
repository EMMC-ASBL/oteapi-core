"""Strategy class for application/vnd.postgresql"""

from typing import Any, Optional

import psycopg
from pydantic import AnyUrl, BaseModel, Field, model_validator
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig


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

        # Copy model-state into placeholders
        accessUrl = AnyUrl(data["accessUrl"])
        default_config = PostgresConfig()
        current_config: dict[str, Any] = data.get("configuration", {})

        if not accessUrl.host:
            raise ValueError("missing host in accessUrl")

        def _get_and_validate_config_value(url_parameter: str, config_key: str) -> str:
            """Get value from accessUrl or current_config, and check for mismatches."""
            value_from_url = getattr(accessUrl, url_parameter, None)
            value_from_config = current_config.get(
                config_key, getattr(default_config, config_key)
            )

            final_value = value_from_url or value_from_config

            if value_from_config and final_value != value_from_config:
                raise ValueError(
                    f"mismatching {url_parameter} in accessUrl and {config_key} in "
                    "configuration"
                )

            return final_value

        user = _get_and_validate_config_value("username", "user")
        password = _get_and_validate_config_value("password", "password")
        dbname = _get_and_validate_config_value("path", "dbname")

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


class AttrDictPostgresResource(AttrDict):
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

    def initialize(self) -> AttrDict:
        """Initialize strategy."""
        return AttrDict()

    def get(self) -> AttrDictPostgresResource:
        """Resource Postgres query responses."""

        connection = create_connection(self.resource_config)
        cursor = connection.cursor()
        result = cursor.execute(self.resource_config.configuration.sqlquery).fetchall()
        connection.close()
        return AttrDictPostgresResource(result=result)
