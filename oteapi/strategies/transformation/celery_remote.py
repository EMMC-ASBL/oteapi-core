"""Transformation Plugin that uses the Celery framework to call remote workers."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Dict

from celery import Celery
from celery.result import AsyncResult
from pydantic import Field
from pydantic.dataclasses import dataclass
import os

from oteapi.models import (
    AttrDict,
    SessionUpdate,
    TransformationConfig,
    TransformationStatus,
)


if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Union

# Connect Celery to the currently running Redis instance

REDIS_HOST = os.environ.get('OTEAPI_REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('OTEAPI_REDIS_PORT', 6379)

CELERY_APP = Celery(broker=f'redis://{REDIS_HOST}:{REDIS_PORT}',
                    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}')


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

    transformationType: str = Field(
        "celery/remote",
        const=True,
        description=TransformationConfig.__fields__[
            "transformationType"
        ].field_info.description,
    )
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

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateCelery:
        """Run a job, return a job ID."""
        celery_kwargs = {}
        if session:
            self._use_session(session)
            celery_kwargs = session.copy()
            for field in CeleryConfig.__fields__:
                celery_kwargs.pop(field, None)

        result: "Union[AsyncResult, Any]" = CELERY_APP.send_task(
            name=self.transformation_config.configuration.task_name,
            args=self.transformation_config.configuration.args,
            kwargs=celery_kwargs,
        )
        return SessionUpdateCelery(data={"task_id":result.task_id})


    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize a job."""
        return SessionUpdate()

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=CELERY_APP)
        return TransformationStatus(id=task_id, status=result.state)

    def _use_session(self, session: "Dict[str, Any]") -> None:
        """Update the configuration with values from the sesssion."""
        for field in CeleryConfig.__fields__:
            if field in session:
                setattr(
                    self.transformation_config.configuration,
                    field,
                    session[field],
                )
