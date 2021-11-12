# pylint: disable=W0511, W0613
"""
Filter plugin for compevo usecase (cropping the image)
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory


class CropDataModel(BaseModel):
    crop: List


@dataclass
@StrategyFactory.register(
    # No other plugin should have filter/compevo-crop!
    ("filterType", "filter/compevo-crop")
)
class CompevoCropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""
        cropData = CropDataModel(**self.filter_config.configuration)
        return dict(crop=cropData.crop)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Crop the image"""
        return {}
