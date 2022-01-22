"""Demo-filter strategy"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, Field

from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import FilterConfig


class CropDataModel(BaseModel):
    """Configuration model for crop data."""

    crop: List[int] = Field(..., description="List of image cropping details.")


@dataclass
@StrategyFactory.register(("filterType", "filter/crop"))
class CropFilter:
    """Strategy for cropping an image.

    **Registers strategies**:

    - `("filterType", "filter/crop")`

    """

    filter_config: "FilterConfig"

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary."""
        return {"result": "collectionid"}

    def get(self, **_) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""
        cropData = (
            CropDataModel(**self.filter_config.configuration)
            if self.filter_config.configuration
            else CropDataModel()
        )
        return {"imagecrop": cropData.crop}
