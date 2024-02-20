"""Function test strategy class."""

from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FunctionConfig

if TYPE_CHECKING:
    pass


@dataclass
class FunctionTestStrategy:
    """Test function strategy."""

    function_config: FunctionConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run function strategy."""
        return AttrDict()
