"""Tranformation Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import SessionUpdate, TransformationConfig, TransformationStatus


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

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "SessionUpdate":
        """Execute the strategy i.e. running a transformation job.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> "SessionUpdate":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """
