# pylint: disable=W0511, W0613
"""
Demo-filter strategy
"""
from typing import Dict, Optional, Any, List
from pydantic import BaseModel
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory
import dlite

class CropDataModel(BaseModel):
    crop: List[int]


@dataclass
@StrategyFactory.register(
    ('filterType', 'filter/compevo-crop') # No other plugin should have filter/compevo-crop!
)
class CropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize strategy and return a dictionary """
        coll = dlite.Collection()
        return dict(collection_id=coll.uuid)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Execute strategy and return a dictionary """

        cropData = CropDataModel(**self.filter_config.configuration)
        retobj = dict(imagecrop=cropData.crop)

        return retobj