#pylint: disable=W0613, W0511
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from app.models.transformationconfig import TransformationConfig, TransformationStatus
from app.strategy.factory import StrategyFactory

@dataclass
@StrategyFactory.register(
    ('transformation_type', 'script/dummy')
)
class DummyTransformationStrategy:
    """ Testing the API """

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Run a job, return a jobid"""
        print ("Running sim...")
        return dict(result="a01d")

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize a job"""
        print ("Initializing")
        # TODO: update with necessary data
        return dict(result="collection id")

    def status(self) -> TransformationStatus:
        """ Get job status """
        ts = TransformationStatus(
            id='0',
            status='wip',
            messages=[],
            created=datetime.utcnow(),
            startTime=datetime.utcnow(),
            finishTime=datetime.utcnow(),
            priority=0,
            secret=None,
            configuration={}
        )
        return ts

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ get transformation """

        # TODO: update and return global state
        return dict()
