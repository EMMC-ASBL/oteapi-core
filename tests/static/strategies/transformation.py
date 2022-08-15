"""Transformation test strategy class."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import TransformationConfig, TransformationStatus

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@dataclass
class TransformationTestStrategy:
    """Test transformation strategy."""

    transformation_config: TransformationConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run transformation strategy."""
        return {}

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run a transformation job."""
        return {}

    def status(self, task_id: str) -> TransformationStatus:
        """Return status for transformation job."""
        return TransformationStatus(id=task_id)
