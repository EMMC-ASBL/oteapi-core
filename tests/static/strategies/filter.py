"""Filter test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig


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
