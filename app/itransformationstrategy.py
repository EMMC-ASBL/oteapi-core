""" Tranformation Strategy Interface
"""

from typing import Protocol, Dict, Optional
from dataclasses import dataclass

@dataclass
class ITransformationStrategy(Protocol): # pylint: disable=R0903
    """ Tranformation Strategy Interfaces """

    configuration: Dict

    def create(self,
        session: Optional[Dict],
    ) -> Dict:
        """ Create a new transformation """


    def run(self) -> str:
        """ Run a job, return jobid """


    def status(self) -> Dict:
        """ Get job status """
