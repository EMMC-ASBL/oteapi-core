"""Demo-filter strategy"""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Tuple

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class CropImageConfig(AttrDict):
    """Configuration model for crop data."""

    crop: Tuple[int, int, int, int] = Field(..., description="Box cropping parameters.")


class CropImageFilterConfig(FilterConfig):
    """Crop filter strategy filter config."""

    configuration: CropImageConfig = Field(
        ..., description="Image crop filter strategy-specific configuration."
    )


@dataclass
class CropImageFilter:
    """Strategy for cropping an image.

    **Registers strategies**:

    - `("filterType", "filter/crop")`

    """

    filter_config: CropImageFilterConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return cropping details."""
        return {"imagecrop": self.filter_config.configuration.crop}
