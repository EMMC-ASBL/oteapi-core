""" Tranformation Strategy Interface
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from oteapi.models.transformationconfig import (
    TransformationConfig,
    TransformationStatus,
)


@dataclass
class ITransformationStrategy(Protocol):  # pylint: disable=R0903
    """Tranformation Strategy Interfaces"""

    transformation_config: TransformationConfig

    def run(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a job, return jobid"""

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status"""

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """get transformation"""

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """initialize transformation"""
