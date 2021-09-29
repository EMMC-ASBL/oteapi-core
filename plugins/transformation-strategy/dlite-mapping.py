from app import factory
from typing import Dict, Optional
from dataclasses import dataclass
import dlite

@dataclass
class DLiteMapping:
    """ Testing the API """

    configuration: Dict

    def create(self,
        session: Optional[Dict]
    ) -> Dict:
        """ Create a new collection if not defined """

        if session:
            if 'collection_id' in session:
                uuid = session['collection_id']
                print ('### using id', uuid)
                collection = dlite.get_collection(uuid)
                return dict(collection_id=collection.uuid)

        collection = dlite.Collection()
        collection.incref()
        print ('### created new collection')

        return dict(collection_id=collection.uuid)


    def run(self) -> str:
        """ Run a job, return a jobid"""
        print ("Running sim...")
        return "a01d"


    def status(self) -> Dict:
        """ Get job status """
        print ("Status Quo")
        return dict(status='ok')


def initialize() -> None:
    factory.register_transformation_strategy("dlite/mapping", DLiteMapping)