# pylint: disable=W0613, W0511
"""
Transformation example (dummy)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import dlite
from oteapi.app.models.transformationconfig import (
    TransformationConfig,
    TransformationStatus,
)
from oteapi.app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("transformation_type", "dlite/transformation"))
class DLiteTransformation:
    """Testing the API"""

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Run a job, return jobid"""
        print("Running")
        return dict(result="0")

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize a job"""
        coll = dlite.Collection()
        return dict(collection_id=coll.uuid)

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status"""
        ts = TransformationStatus(
            id=task_id,
            status="WiP",
            messages=[],
            created=datetime.utcnow(),
            startTime=datetime.utcnow(),
            finishTime=datetime.utcnow(),
        )

        return ts

    def get(self, session_id: Optional[str] = None) -> Dict:
        """get transformation"""

        # TODO: update and return global state
        return dict()
