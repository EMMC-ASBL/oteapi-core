"""Transformation Plugin that uses the Celery framework to call remote workers."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Dict

from celery import Celery
from celery.result import AsyncResult
from fastapi_plugins import RedisSettings
from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import (
    AttrDict,
    SessionUpdate,
    TransformationConfig,
    TransformationStatus,
)

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Union

# Connect Celery to the currently running Redis instance
CELERY = Celery(broker=RedisSettings().redis_url, backend=RedisSettings().redis_url)


class CeleryConfig(AttrDict):
    """Celery configuration."""

    task_name: str = Field(..., description="A task name.")
    args: list = Field(..., description="List of arguments for the task.")


class SessionUpdateCelery(SessionUpdate):
    """Class for returning values from XLSXParse."""

    data: Dict[str, list] = Field(
        ...,
        description="A dict with column-name/column-value pairs. The values are lists.",
    )


class CeleryStrategyConfig(TransformationConfig):
    """Celery strategy-specific configuration."""

    configuration: CeleryConfig = Field(
        ..., description="Celery transformation strategy-specific configuration."
    )


@dataclass
class CeleryRemoteStrategy:
    """Submit job to remote Celery runner.

    **Registers strategies**:

    - `("transformationType", "celery/remote")`

    """

    transformation_config: CeleryStrategyConfig

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> TransformationStatus:
        """Run a job, return a job ID."""
        if session:
            self._use_session(session)
            celery_kwargs = session.copy()
            for field in CeleryConfig.__fields__:
                celery_kwargs.pop(field, None)

        result: "Union[AsyncResult, Any]" = CELERY.send_task(
            name=self.transformation_config.configuration.task_name,
            args=self.transformation_config.configuration.args,
            kwargs=celery_kwargs,
        )
        return self.status(result.task_id)

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize a job."""
        return SessionUpdate()

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=CELERY)
        return TransformationStatus(id=task_id, status=result.state)

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateCelery:
        """Get transformation."""
        # TODO: update and return global state  # pylint: disable=fixme
        return SessionUpdateCelery(data={})

    def _use_session(self, session: "Dict[str, Any]") -> None:
        """Update the configuration with values from the sesssion."""
        for field in CeleryConfig.__fields__:
            if field in session:
                setattr(
                    self.transformation_config.configuration,
                    field,
                    session[field],
                )
