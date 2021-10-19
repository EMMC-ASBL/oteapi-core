# pylint: disable=W0511, W0613
"""
Demo-filter strategy
"""
from typing import Dict, Optional, Any, List
from pydantic import BaseModel
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy import factory

class CropDataModel(BaseModel):
    crop: List[int]

@dataclass
class CropFilter:

    filter_config : FilterConfig

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Execute strategy and return a dictionary """

        cropData = CropDataModel(**self.filter_config.configuration)
        retobj = dict(imagecrop=cropData.crop)

        return retobj

def initialize() -> None:
    factory.register_filter_strategy("filter/crop", CropFilter)