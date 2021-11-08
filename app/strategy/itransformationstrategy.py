""" Tranformation Strategy Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from app.models.transformationconfig import TransformationConfig, TransformationStatus
from app.strategy.factory import StrategyFactory


@dataclass
class ITransformationStrategy(Protocol):  # pylint: disable=R0903
    """Tranformation Strategy Interfaces"""

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Run a job, return jobid"""

    def status(self) -> TransformationStatus:
        """Get job status"""

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """get transformation"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """initialize transformation"""


def create_transformation_strategy(
    transformation_config: TransformationConfig,
) -> ITransformationStrategy:
    """Helper function to instanciate a transformation strategy"""
    return StrategyFactory.make_strategy(transformation_config, "transformation_type")
