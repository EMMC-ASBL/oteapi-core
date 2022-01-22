"""Transformation Plugin that uses the Celery framework to call remote workers."""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, List

from celery import Celery
from celery.result import AsyncResult
from fastapi_plugins import RedisSettings
from pydantic import BaseModel

from oteapi.models import TransformationStatus
from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Dict, Optional

    from oteapi.models import TransformationConfig

# Connect Celery to the currently running Redis instance
app = Celery(broker=RedisSettings().redis_url, backend=RedisSettings().redis_url)


class CeleryConfig(BaseModel):
    """Celery configuration.

    Attributes:
        taskName: A task name.
        args: List of arguments for the task.

    """

    taskName: str
    args: List[Any]


@dataclass
@StrategyFactory.register(("transformation_type", "celery/remote"))
class CeleryRemoteStrategy:
    """Submit job to remote Celery runner.

    **Registers strategies**:

    - `("transformation_type", "celery/remote")`

    """

    transformation_config: "TransformationConfig"

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run a job, return a job ID."""
        config = self.transformation_config.configuration
        celeryConfig = CeleryConfig() if config is None else CeleryConfig(**config)
        result = app.send_task(celeryConfig.taskName, celeryConfig.args, kwargs=session)
        return {"result": result.task_id}

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize a job."""
        return {}

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=app)
        return TransformationStatus(id=task_id, status=result.state)

    def get(self, **_) -> "Dict[str, Any]":
        """Get transformation."""
        # TODO: update and return global state  # pylint: disable=fixme
        return {}
