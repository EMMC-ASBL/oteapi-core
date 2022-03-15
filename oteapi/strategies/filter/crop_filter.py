"""Demo-filter strategy"""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Tuple

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, FilterConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class CropImageConfig(AttrDict):
    """Configuration model for crop data."""

    crop: Tuple[int, int, int, int] = Field(
        ..., description="Box cropping parameters (left, top, right, bottom)."
    )


class CropImageFilterConfig(FilterConfig):
    """Crop filter strategy filter config."""

    filterType: str = Field(
        "filter/crop",
        const=True,
        description=FilterConfig.__fields__["filterType"].field_info.description,
    )
    configuration: CropImageConfig = Field(
        ..., description="Image crop filter strategy-specific configuration."
    )


class SessionUpdateCropFilter(SessionUpdate):
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

    def initialize(
        self,
        session: "Optional[Dict[str, Any]]" = None,
    ) -> SessionUpdateCropFilter:
        """Initialize strategy and return a dictionary."""
        return SessionUpdateCropFilter(
            imagecrop=self.filter_config.configuration.crop,
        )

    def get(
        self,
        session: "Optional[Dict[str, Any]]" = None,
    ) -> SessionUpdate:
        """Execute strategy and return a dictionary"""
        return SessionUpdate()
