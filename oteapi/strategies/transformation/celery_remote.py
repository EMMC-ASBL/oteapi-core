"""Transformation Plugin that uses the Celery framework to call remote workers."""

import os
from typing import TYPE_CHECKING, Literal

from celery import Celery
from celery.result import AsyncResult
from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, TransformationConfig, TransformationStatus

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Union

# Connect Celery to the currently running Redis instance

REDIS_HOST = os.getenv("OTEAPI_REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("OTEAPI_REDIS_PORT", "6379"))

CELERY_APP = Celery(
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


class CeleryConfig(AttrDict):
    """Celery configuration.

    All fields here (including those added from the session through the `get()` method,
    as well as those added "anonymously") will be used as keyword arguments to the
    `send_task()` method for the Celery App.

    Note:
        Using `alias` for the `name` field to favor populating it with `task_name`
        arguments, since this is the "original" field name. I.e., this is done for
        backwards compatibility.

    Special pydantic configuration settings:

    - **`populate_by_name`**
      Allow populating CeleryConfig.name using `name` as well as `task_name`.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., description="A task name.", alias="task_name")
    args: list = Field(..., description="List of arguments for the task.")


class AttrDictCelery(AttrDict):
    """Class for returning values from a Celery task."""

    celery_task_id: str = Field(..., description="A Celery task identifier.")


class CeleryStrategyConfig(TransformationConfig):
    """Celery strategy-specific configuration."""

    transformationType: Literal["celery/remote"] = Field(
        "celery/remote",
        description=TransformationConfig.model_fields["transformationType"].description,
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

    def get(self) -> AttrDictCelery:
        """Run a job, return a job ID."""

        result: "Union[AsyncResult, Any]" = CELERY_APP.send_task(
            **self.transformation_config.configuration.model_dump()
        )
        return AttrDictCelery(celery_task_id=result.task_id)

    def initialize(self) -> AttrDict:
        """Initialize a job."""
        return AttrDict()

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=CELERY_APP)
        return TransformationStatus(id=task_id, status=result.state)
