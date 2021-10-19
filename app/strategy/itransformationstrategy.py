""" Tranformation Strategy Interface
"""

from typing import Protocol, Dict, Optional, Any
from dataclasses import dataclass
from app.models.transformationconfig import TransformationConfig, TransformationStatus

@dataclass
class ITransformationStrategy(Protocol): # pylint: disable=R0903
    """ Tranformation Strategy Interfaces """

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Run a job, return jobid """


    def status(self) -> TransformationStatus:
        """ Get job status """


    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ get transformation """
