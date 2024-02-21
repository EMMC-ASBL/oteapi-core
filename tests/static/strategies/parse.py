"""Parse test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ResourceConfig


@dataclass
class ParseTestStrategy:
    """Test parse strategy."""

    parse_config: ResourceConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run parse strategy."""
        return AttrDict()
