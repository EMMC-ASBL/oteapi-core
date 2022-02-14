"""Demo-filter strategy"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from pydantic import Field

from oteapi.models import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import FilterConfig


class SessionUpdateCrop(SessionUpdate):
    """Class for returning values from crop data."""

    crop: List[int] = Field(..., description="List of image cropping details.")


@dataclass
class CropFilter:
    """Strategy for cropping an image.

    **Registers strategies**:

    - `("filterType", "filter/crop")`

    """

    filter_config: "FilterConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy and return a dictionary."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateCrop:
        """Execute strategy and return a dictionary"""
        cropData = (
            SessionUpdateCrop(**self.filter_config.configuration.dict())
            if self.filter_config.configuration
            else SessionUpdateCrop()
        )
        return cropData
