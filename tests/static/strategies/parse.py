"""Parse test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ParserConfig


@dataclass
class ParseTestStrategy:
    """Test parse strategy."""

    parse_config: ParserConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run parse strategy."""
        return AttrDict()
