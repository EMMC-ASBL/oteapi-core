"""Mapping test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, MappingConfig


@dataclass
class MappingTestStrategy:
    """Test mapping strategy."""

    mapping_config: MappingConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run mapping strategy."""
        return AttrDict()
