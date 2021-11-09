# pylint: disable=W0511, W0613
"""
Demo-filter strategy
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory


class CropDataModel(BaseModel):
    crop: List[int]


@dataclass
@StrategyFactory.register(("filterType", "filter/crop"))
class CropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize strategy and return a dictionary"""

        # TODO: Add logic
        return dict(result="collectionid")

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Execute strategy and return a dictionary"""

        cropData = CropDataModel(**self.filter_config.configuration)
        retobj = dict(imagecrop=cropData.crop)

        return retobj
