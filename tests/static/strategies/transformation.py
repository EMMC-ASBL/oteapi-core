"""Transformation test strategy class."""

from __future__ import annotations

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, TransformationConfig, TransformationStatus


@dataclass
class TransformationTestStrategy:
    """Test transformation strategy."""

    transformation_config: TransformationConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run transformation strategy."""
        return AttrDict()

    def status(self, task_id: str) -> TransformationStatus:
        """Return status for transformation job."""
        return TransformationStatus(id=task_id)
