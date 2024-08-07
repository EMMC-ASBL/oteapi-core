"""Function test strategy class."""

from __future__ import annotations

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FunctionConfig


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
