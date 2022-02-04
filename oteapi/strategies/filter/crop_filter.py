"""Demo-filter strategy"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, Field

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import FilterConfig


class CropDataModel(BaseModel):
    """Configuration model for crop data."""

    crop: List[int] = Field(..., description="List of image cropping details.")


@dataclass
class CropFilter:
    """Strategy for cropping an image.

    **Registers strategies**:

    - `("filterType", "filter/crop")`

    """

    filter_config: "FilterConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary."""
        return {"result": "collectionid"}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""
        cropData = (
            CropDataModel(**self.filter_config.configuration)
            if self.filter_config.configuration
            else CropDataModel()
        )
        return {"imagecrop": cropData.crop}
