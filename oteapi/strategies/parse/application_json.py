"""Strategy class for application/json."""
import json
from typing import Literal, Optional

from pydantic import Field, AnyHttpUrl
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig
from oteapi.models.parserconfig import ParserConfig
from oteapi.plugins import create_strategy


class JSONConfig(AttrDict):
    """JSON parse-specific Configuration Data Model."""
        
    downloadUrl: Optional[AnyHttpUrl] = Field(
        None,
        description="The HTTP(S) URL, which will be downloaded."
    )
    mediaType: Optional[str] = Field(
        "application/json",
        description=(
            "The media type"
        ),
    )
    datacache_config: Optional[DataCacheConfig] = Field(
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


class AttrDictJSONParse(AttrDict):
    """Class for returning values from JSON Parse."""

    content: dict = Field(..., description="Content of the JSON document.")


@dataclass
class JSONDataParseStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("strategyType", "parser/json")`

    """

    parse_config: JSONParserConfig

    def initialize(self) -> AttrDictJSONParse:
        """Initialize."""
        return AttrDictJSONParse(content={})

    def get(self) -> AttrDictJSONParse:
        """Parse json."""
        downloader = create_strategy("download", dict(self.parse_config.configuration))
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration.datacache_config)
        content = cache.get(output["key"])

        if isinstance(content, dict):
            return AttrDictJSONParse(content=content)
        return AttrDictJSONParse(content=json.loads(content))
    