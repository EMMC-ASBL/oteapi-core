"""Tranformation Strategy Interface"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import TransformationConfig, TransformationStatus


@dataclass  # type: ignore[misc]
class ITransformationStrategy(Protocol):
    """Tranformation Interfaces"""

    transformation_config: "TransformationConfig"

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run a job, return jobid"""

    def status(self, task_id: str) -> "TransformationStatus":
        """Get job status"""

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """get transformation"""

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """initialize transformation"""
