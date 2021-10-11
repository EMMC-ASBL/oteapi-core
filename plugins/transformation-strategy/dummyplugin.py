from app.strategy import factory
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class DummyTransformationStrategy:
    """ Testing the API """

    configuration: Dict


    def create(self,
        session: Optional[Dict]
    ) -> Dict:
        """ Create a new dummy process """

        print ("Creating a new job:", self.configuration)
        if session:
            print (session)
        return dict(status='ok')


    def run(self) -> str:
        """ Run a job, return a jobid"""
        print ("Running sim...")
        return "a01d"


    def status(self) -> Dict:
        """ Get job status """
        print ("Status Quo")
        return dict(status='ok')


def initialize() -> None:
    factory.register_transformation_strategy("script/dummy", DummyTransformationStrategy)