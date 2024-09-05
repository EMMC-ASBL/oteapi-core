"""Strategy class for application/vnd.sqlite3."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import (
    AttrDict,
    DataCacheConfig,
    HostlessAnyUrl,
    ParserConfig,
    ResourceConfig,
)
from oteapi.plugins import create_strategy


class SqliteConfig(AttrDict):
    """Configuration data model for
    [`SqliteParseStrategy`][oteapi.strategies.parse.application_vnd_sqlite.SqliteParseStrategy].
    """

    # Resource config
    downloadUrl: Optional[HostlessAnyUrl] = Field(
        None, description=ResourceConfig.model_fields["downloadUrl"].description
    )
    mediaType: Literal["application/vnd.sqlite3"] = Field(
        "application/vnd.sqlite3",
        description=ResourceConfig.model_fields["mediaType"].description,
    )

    # SQLite parse strategy-specific config
    sqlquery: str = Field("", description="A SQL query string.")
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )


class SqliteParserConfig(ParserConfig):
    """SQLite parse strategy resource config."""

    parserType: Literal["parser/sqlite3"] = Field(
        "parser/sqlite3",
        description=ParserConfig.model_fields["parserType"].description,
    )
    configuration: SqliteConfig = Field(
        ..., description="SQLite parse strategy-specific configuration."
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


class SqLiteParseContent(AttrDict):
    """Configuration model for SqLiteParse."""

    result: list = Field(..., description="List of results from the query.")


@dataclass
class SqliteParseStrategy:
    """Parse strategy for SQLite.

    Purpose of this strategy: Download a SQLite database using `downloadUrl` and run a
    SQL query on the database to return all relevant rows.

    """

    parse_config: SqliteParserConfig

    def initialize(self) -> AttrDict:
        """Initialize strategy."""
        return AttrDict()

    def get(self) -> SqLiteParseContent:
        """Parse SQLite query responses."""

        if self.parse_config.configuration.downloadUrl is None:
            raise ValueError("No download URL provided.")

        if self.parse_config.configuration.mediaType != "application/vnd.sqlite3":
            raise ValueError("Invalid media type.")

        # Retrieve SQLite file
        downloader = create_strategy(
            "download", self.parse_config.configuration.model_dump()
        )
        cache_key = downloader.get()["key"]

        cache = DataCache(self.parse_config.configuration.datacache_config)
        with cache.getfile(cache_key, suffix="db") as filename:
            connection = create_connection(filename)
            cursor = connection.cursor()
            result = cursor.execute(self.parse_config.configuration.sqlquery).fetchall()
            connection.close()
        return SqLiteParseContent(result=result)
