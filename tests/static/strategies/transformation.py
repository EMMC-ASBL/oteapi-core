"""Transformation test strategy class."""
from typing import TYPE_CHECKING

from oteapi.models import TransformationConfig, TransformationStatus
from oteapi.utils._pydantic import dataclasses as pydantic_dataclasses

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@pydantic_dataclasses.dataclass
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

    def status(self, task_id: str) -> TransformationStatus:
        """Return status for transformation job."""
        return TransformationStatus(id=task_id)
