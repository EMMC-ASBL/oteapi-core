"""Filter test strategy class."""

from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig

if TYPE_CHECKING:
    pass


@dataclass
class FilterTestStrategy:
    """Test filter strategy."""

    filter_config: FilterConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run filter strategy."""
        return AttrDict()
