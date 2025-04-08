"""Strategy class for application/json."""

from __future__ import annotations

import json
from typing import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, HostlessAnyUrl, ParserConfig
from oteapi.plugins import create_strategy


class JSONConfig(AttrDict):
    """JSON parse-specific Configuration Data Model."""

    downloadUrl: HostlessAnyUrl | None = Field(
        None, description="The HTTP(S) URL, which will be downloaded."
    )
    mediaType: Literal["application/json"] = Field(
        "application/json",
        description=("The media type"),
    )
    datacache_config: DataCacheConfig | None = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )


class JSONParserConfig(ParserConfig):
    """JSON parse strategy filter config."""

    parserType: Literal["parser/json"] = Field(
        "parser/json",
        description=ParserConfig.model_fields["parserType"].description,
    )
    configuration: JSONConfig = Field(
        ..., description="JSON parse strategy-specific configuration."
    )


class JSONParseContent(AttrDict):
    """Class for returning values from JSON Parse."""

    content: dict = Field(..., description="Content of the JSON document.")


@dataclass
class JSONDataParseStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("parserType", "parser/json")`

    """

    parse_config: JSONParserConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> JSONParseContent:
        """Parse json."""
        downloader = create_strategy(
            "download", self.parse_config.configuration.model_dump()
        )
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration.datacache_config)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return JSONParseContent(content=content)
        return JSONParseContent(content=json.loads(content))
