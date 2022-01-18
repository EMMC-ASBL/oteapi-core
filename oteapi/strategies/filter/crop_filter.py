"""Demo-filter strategy"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from oteapi.models.filterconfig import FilterConfig
from oteapi.plugins.factories import StrategyFactory


class CropDataModel(BaseModel):
    crop: List[int]


@dataclass
@StrategyFactory.register(("filterType", "filter/crop"))
class CropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize strategy and return a dictionary"""
        return {"result": "collectionid"}

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute strategy and return a dictionary"""
        cropData = CropDataModel(**self.filter_config.configuration)
        return {"imagecrop": cropData.crop}
