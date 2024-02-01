"""Resource test strategy class."""
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ResourceConfig

if TYPE_CHECKING:
    pass


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
