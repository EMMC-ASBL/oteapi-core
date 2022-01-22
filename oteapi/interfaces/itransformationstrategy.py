"""Tranformation Strategy Interface"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import TransformationConfig, TransformationStatus


@dataclass  # type: ignore[misc]
@runtime_checkable
class ITransformationStrategy(Protocol):
    """Transformation Strategy Interface."""

    transformation_config: "TransformationConfig"

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run a transformation job.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.
            As a minimum, the dictionary will contain the job ID.

        """

    def status(self, task_id: str) -> "TransformationStatus":
        """Get job status.

        Parameters:
            task_id: The transformation job ID.
            session: A session-specific dictionary context.

        Returns:
            An overview of the transformation job's status, including relevant
            metadata.

        """

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute the strategy.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """
