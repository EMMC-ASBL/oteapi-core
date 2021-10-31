# pylint: disable=W0511, W0613
"""
Filter plugin for compevo usecase (store the image in dlite)
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from app.models.filterconfig import FilterConfig
from app.strategy.factory import StrategyFactory
import dlite


@dataclass
@StrategyFactory.register(
    # No other plugin should have filter/compevo-crop!
    ('filterType', 'filter/compevo-store')
)
class CompevoCropFilter:

    filter_config: FilterConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize strategy and return a dictionary """
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Store the image in dlite  """
        coll=dlite.get_collection(session['collection_id'])
        filename=session['filename']
        dlite.storage_path.append(str('app/entities/*.json'))
        inst = dlite.Instance('blob:' +  filename)
        coll.add('blob', inst)
        return dict(FilterStoreStep='compevo-store')
