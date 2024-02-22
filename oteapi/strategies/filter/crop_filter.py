"""Demo-filter strategy"""

from typing import Literal, Optional, Tuple

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig


class CropImageConfig(AttrDict):
    """Configuration model for crop data."""

    crop: Optional[Tuple[int, int, int, int]] = Field(
        None, description="Box cropping parameters (left, top, right, bottom)."
    )


class CropImageFilterConfig(FilterConfig):
    """Crop filter strategy filter config."""

    filterType: Literal["filter/crop"] = Field(
        "filter/crop",
        description=FilterConfig.model_fields["filterType"].description,
    )
    configuration: CropImageConfig = Field(
        ..., description="Image crop filter strategy-specific configuration."
    )


class CropFilterContent(AttrDict):
    """Return model for `CropImageFilter`."""

    imagecrop: Tuple[int, int, int, int] = Field(
        ..., description="Box cropping parameters (left, top, right, bottom)."
    )


@dataclass
class CropImageFilter:
    """Strategy for cropping an image.

    **Registers strategies**:

    - `("filterType", "filter/crop")`

    """

    filter_config: CropImageFilterConfig

    def initialize(self) -> CropFilterContent:
        """Initialize strategy and return a dictionary."""
        if self.filter_config.configuration.crop is None:
            raise ValueError("Crop filter requires crop configuration.")

        return CropFilterContent(
            imagecrop=self.filter_config.configuration.crop,
        )

    def get(self) -> AttrDict:
        """Execute strategy and return a dictionary"""
        return AttrDict()
