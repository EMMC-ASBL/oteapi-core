"""Resource test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ResourceConfig


@dataclass
class ResourceTestStrategy:
    """Test resource strategy."""

    resource_config: ResourceConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run resource strategy."""
        return AttrDict()
