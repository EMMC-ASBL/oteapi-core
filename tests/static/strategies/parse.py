"""Parse test strategy class."""
from typing import TYPE_CHECKING

from oteapi.models import ResourceConfig
from oteapi.utils._pydantic import dataclasses as pydantic_dataclasses

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@pydantic_dataclasses.dataclass
class ParseTestStrategy:
    """Test parse strategy."""

    parse_config: ResourceConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run parse strategy."""
        return {}
