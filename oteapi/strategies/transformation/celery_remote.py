"""Transformation Plugin that uses the Celery framework to call remote workers."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from celery import Celery
from celery.result import AsyncResult
from fastapi_plugins import RedisSettings
from pydantic import BaseModel

from oteapi.models.transformationconfig import (
    TransformationConfig,
    TransformationStatus,
)
from oteapi.plugins.factories import StrategyFactory

# Connect Celery to the currently running Redis instance
app = Celery(broker=RedisSettings().redis_url, backend=RedisSettings().redis_url)


class CeleryConfig(BaseModel):
    taskName: str
    args: List[Any]


@dataclass
@StrategyFactory.register(("transformation_type", "celery/remote"))
class CeleryRemoteStrategy:
    """Submit job to remote runner"""

    transformation_config: TransformationConfig

    def run(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Run a job, return a jobid"""
        config = self.transformation_config.configuration
        celeryConfig = CeleryConfig(**config)
        result = app.send_task(
            celeryConfig.taskName, celeryConfig.args, kwargs=session_id
        )
        return {"result": result.task_id}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize a job"""
        return {}

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status"""
        result = AsyncResult(id=task_id, app=app)
        return TransformationStatus(id=task_id, status=result.state)

    def get(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get transformation."""
        # TODO: update and return global state  # pylint: disable=fixme
        return {}
