"""Mapping test strategy class."""
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, MappingConfig

if TYPE_CHECKING:
    pass


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
