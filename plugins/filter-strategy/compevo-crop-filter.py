# pylint: disable=W0511, W0613
"""
Filter plugin for compevo usecase (cropping the image)
"""
from typing import Dict, Optional, Any
from pydantic import BaseModel
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory
import dlite


class CropDataModel(BaseModel):
    crop: str


@dataclass
@StrategyFactory.register(
    # No other plugin should have filter/compevo-crop!
    ('filterType', 'filter/compevo-crop')
)
class CompevoCropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize strategy and return a dictionary """
        cropData = CropDataModel(**self.filter_config.configuration)
        return dict(crop=cropData.crop)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Crop the image """
        coll = dlite.get_collection(session['collection_id'])
        image = coll.get('pore_image')
        coll.remove('pore_image')
        r = coll.find_first(s='pore_image', p='crop')
        x1, x2, y1, y2 = [int(i) for i in r.o.split(',')]
        data = image.data[y1:y2, x1:x2]
        cropped = dlite.Instance(image.meta.uri, data.shape)
        cropped.data = data
        cropped.scale = image.scale
        coll.add('pore_image', cropped)
        return dict(FilterCropStep='compevo-crop')
