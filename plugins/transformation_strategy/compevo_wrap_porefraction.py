# pylint: disable=W0613, W1510, W0611, W0511
"""
Transformation plugin for compevo usecase (wrap porefraction)
"""

import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

import dlite
from matplotlib.pyplot import imsave

from app.models.transformationconfig import TransformationConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("transformation_type", "dlite/compevo-wrap-porefraction"))
class WrapPorefractionTransformation:
    """Transformations"""

    transformation_config: TransformationConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize a job"""
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Wrap porefraction transformation"""

        coll = dlite.get_collection(session["collection_id"])
        dlite.storage_path.append(str("app/entities/*.json"))

        image = coll.get("pore_image")
        imsave("/ote-data/pore_image.tiff", image.data)

        args = [
            sys.executable,
            "/app/cache/compevo/porefraction.py",
            "/ote-data/pore_image.tiff",
        ]
        output = subprocess.run(args, capture_output=True)
        pore_fraction = float((output.stdout))
        pf = dlite.Instance("http://compevo/ontotrans.emmc.eu/0.1/PoreFraction", [])
        pf.pore_fraction = pore_fraction
        coll.add("pore_fraction", pf)

        return dict(TransformationStep="compevo-wrap-porefraction")
