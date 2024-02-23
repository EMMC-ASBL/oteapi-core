"""Tranformation Strategy Interface"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.models import AttrDict, TransformationConfig, TransformationStatus


@dataclass  # type: ignore[misc]
class ITransformationStrategy(Protocol):
    """Transformation Strategy Interface."""

    transformation_config: "TransformationConfig"

    def status(self, task_id: str) -> "TransformationStatus":
        """Get job status.

        Parameters:
            task_id: The transformation job ID.

        Returns:
            An overview of the transformation job's status, including relevant
            metadata.

        """

    def get(self) -> "AttrDict":
        """Execute the strategy i.e. running a transformation job.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

    def initialize(self) -> "AttrDict":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """
