"""Transformation test strategy class."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import TransformationConfig, TransformationStatus


@dataclass
class TransformationTestStrategy:
    """Test transformation strategy."""

    transformation_config: "TransformationConfig"

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

    def status(self, task_id: str) -> "TransformationStatus":
        """Return status for transformation job.

        NOTE: The `TransformationStatus` is imported properly within this method to
            avoid importing anything from the `oteapi` package unnecessarily when
            testing.
        """
        from oteapi.models.transformationconfig import TransformationStatus

        return TransformationStatus(id=task_id)
