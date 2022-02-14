"""Transformation Plugin that uses the Celery framework to call remote workers."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from celery import Celery
from celery.result import AsyncResult
from fastapi_plugins import RedisSettings
from pydantic import BaseModel, Field

from oteapi.models import SessionUpdate, TransformationStatus

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Union

    from oteapi.models import TransformationConfig

# Connect Celery to the currently running Redis instance
app = Celery(broker=RedisSettings().redis_url, backend=RedisSettings().redis_url)


class SessionUpdateCelery(SessionUpdate):
    """Class for returning values from XLSXParse."""

    data: Dict[str, list] = Field(
        ...,
        description="A dict with column-name/column-value pairs. The values are lists.",
    )


class CeleryConfig(BaseModel):
    """Celery configuration."""

    task_name: str = Field(..., description="A task name.")
    args: list = Field(..., description="List of arguments for the task.")


@dataclass
class CeleryRemoteStrategy:
    """Submit job to remote Celery runner.

    **Registers strategies**:

    - `("transformationType", "celery/remote")`

    """

    transformation_config: "TransformationConfig"

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> TransformationStatus:
        """Run a job, return a job ID."""
        config = self.transformation_config.configuration
        celery_config = CeleryConfig() if config is None else CeleryConfig(**config)
        result: "Union[AsyncResult, Any]" = app.send_task(
            celery_config.task_name, celery_config.args, kwargs=session
        )
        status = AsyncResult(id=result.task_id, app=app)
        return TransformationStatus(id=result.task_id, status=status.status)

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize a job."""
        return SessionUpdate()

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=app)
        return TransformationStatus(id=task_id, status=result.state)

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "SessionUpdateCelery":
        """Get transformation."""
        # TODO: update and return global state  # pylint: disable=fixme
        return SessionUpdateCelery(data={})
