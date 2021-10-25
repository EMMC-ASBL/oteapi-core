# pylint: disable=W0511, W0613
"""
Demo-filter strategy
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
    ('filterType', 'filter/compevo-crop') # No other plugin should have filter/compevo-crop!
)
class CompevoCropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize strategy and return a dictionary """
        cropData = CropDataModel(**self.filter_config.configuration)
        return dict( crop=cropData.crop)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Execute strategy and return a dictionary """

               
        coll = dlite.get_collection(session['collection_id']) #pylint: disable=W0612
        
        image = coll.get('pore_image')

        coll.remove('pore_image')

        r = coll.find_first(s='pore_image', p='crop')
        x1, x2, y1, y2 = [int(i) for i in r.o.split(',')]
        data = image.data[y1:y2, x1:x2]
        cropped = dlite.Instance(image.meta.uri, data.shape)
        cropped.data = data
        cropped.scale = image.scale
        coll.add('pore_image', cropped)
        return dict(filetrstep='filterstep')
