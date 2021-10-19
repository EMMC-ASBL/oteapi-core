#pylint: disable=W0613, W0511
"""
Transformation example (dummy)
"""
from app.strategy import factory
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from app.models.transformationconfig import TransformationConfig, TransformationStatus


@dataclass
class DLiteTransformation:
    """ Testing the API """

    transformation_config: TransformationConfig

    def run(self, session_id: Optional[str] = None) -> str:
        """ Run a job, return jobid """
        print ("Running")
        return "0"


    def status(self) -> TransformationStatus:
        """ Get job status """
        ts = TransformationStatus(
            id = "0",
            status = "WiP",
            messages = [],
            created = datetime.utcnow(),
            startTime = datetime.utcnow(),
            finishTime = datetime.utcnow()
        )

        return ts


    def get(self, session_id: Optional[str] = None) -> Dict:
        """ get transformation """

        # TODO: update and return global state
        return dict()

def initialize() -> None:
    factory.register_transformation_strategy("dlite/transformation", DLiteTransformation)