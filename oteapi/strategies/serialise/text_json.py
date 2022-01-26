"""Strategy class for serialising text/json."""
# pylint: disable=unused-argument
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from oteapi.datacache import DataCache
from oteapi.models import DataCacheConfig
from oteapi.plugins.factories import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


class JSONSerialiseConfig(BaseModel):
    """File-specific Configuration Data Model."""

    accessKey: str = Field(
        ..., description="Datacache key to the Python object that should be serialised."
    )
    datacache: Optional[DataCacheConfig] = Field(
        {},
        description=(
            "Configuration of the datacache entry that will be created "
            "for the serialised content."
        ),
    )


@dataclass
@StrategyFactory.register(("mediaType", "text/json"))
class JSONSerialiseStrategy:
    """Serialise strategy for JSON.

    **Registers strategies**:

    - `("mediaType", "text/json")`

    """

    resource_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def parse(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Serialise json.

        Loads a Python (JSON sieialisable) object from the data cache
        (using `resource_config.configuration.accessKey`), converts it
        to JSON and stores the new string in datacache under the
        returned key.

        Args:
            session: Optional session. Currently unused.

        Returns:
            A dict `{"key": datacache_key}` where `datacache_key` is a
            key to the serialised content stored in the data cache.
        """
        config = JSONSerialiseConfig(self.resource_config.configuration)
        cache = DataCache(config.datacache)
        obj = cache.get(config.accessKey)
        jsn = json.dumps(obj)
        key = cache.add(jsn)
        return {"key": key}
