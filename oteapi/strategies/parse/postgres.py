"""Strategy class for application/vnd.postgresql"""

from __future__ import annotations

import sys
from typing import Any, Optional

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

import psycopg
from pydantic import AnyUrl, BaseModel, Field, model_validator
from pydantic.dataclasses import dataclass

from oteapi.models import (
    AttrDict,
    DataCacheConfig,
    HostlessAnyUrl,
    ParserConfig,
    ResourceConfig,
)


class PostgresConfig(AttrDict):
    """Configuration data model for
    [`PostgresParserStrategy`][oteapi.strategies.parse.postgres.PostgresParserConfig].
    """

    # Resource config
    accessService: Literal["postgres"] = Field(
        "postgres",
        description=ResourceConfig.model_fields["accessService"].description,
    )
    accessUrl: Optional[HostlessAnyUrl] = Field(
        None,
        description=ResourceConfig.model_fields["accessUrl"].description,
    )

    # Postgres specific config
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )
    user: Optional[str] = Field(None, description="postgres server username")
    dbname: Optional[str] = Field(None, description="postgres dbname name")
    password: Optional[str] = Field(None, description="postgres password")
    sqlquery: str = Field("", description="A SQL query string.")

    @model_validator(mode="before")
    @classmethod
    def adjust_url(cls, data: Any) -> dict[str, Any]:
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
            return data

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


class PostgresParserConfig(ParserConfig):
    """Postgresql parse strategy config"""

    parserType: Literal["parser/postgres"] = Field(
        "parser/postgres",
        description="Type of registered resource strategy.",
    )
    configuration: PostgresConfig = Field(
        ...,
        description=(
            "Configuration for resource. Values in the accessURL take precedence."
        ),
    )


def create_connection(url: str) -> psycopg.Connection:
    """Create a dbname connection to Postgres dbname.

    Parameters:
        url: A valid PostgreSQL URL.

    Raises:
        psycopg.Error: If a DB connection cannot be made.

    Returns:
        Connection object.

    """
    try:
        return psycopg.connect(url)
    except psycopg.Error as exc:
        raise psycopg.Error("Could not connect to given Postgres DB.") from exc


class PostgresParserContent(AttrDict):
    """Configuration model for PostgresParser."""

    result: list = Field(..., description="List of results from the query.")


@dataclass
class PostgresParserStrategy:
    """Resource strategy for Postgres.

    Purpose of this strategy: Connect to a postgres DB and run a
    SQL query on the dbname to return all relevant rows.

    """

    parser_config: PostgresParserConfig

    def initialize(self) -> AttrDict:
        """Initialize strategy."""
        return AttrDict()

    def get(self) -> PostgresParserContent:
        """Resource Postgres query responses."""

        if self.parser_config.configuration.accessUrl is None:
            raise ValueError("accessUrl is required for PostgresParserStrategy")

        connection = create_connection(str(self.parser_config.configuration.accessUrl))
        cursor = connection.cursor()
        result = cursor.execute(self.parser_config.configuration.sqlquery).fetchall()
        connection.close()
        return PostgresParserContent(result=result)
