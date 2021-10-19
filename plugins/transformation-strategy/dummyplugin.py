#pylint: disable=W0613, W0511
from app.strategy import factory
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from app.models.transformationconfig import TransformationConfig, TransformationStatus

@dataclass
class DummyTransformationStrategy:
    """ Testing the API """

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Run a job, return a jobid"""
        print ("Running sim...")
        return "a01d"


    def status(self) -> TransformationStatus:
        """ Get job status """
        ts = TransformationStatus(
            id='0',
            status='wip',
            messages=[],
            created=datetime.utcnow(),
            priority=0,
            secret=None,
            configuration={}
        )
        return ts

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ get transformation """

        # TODO: update and return global state
        return dict()

def initialize() -> None:
    factory.register_transformation_strategy("script/dummy", DummyTransformationStrategy)