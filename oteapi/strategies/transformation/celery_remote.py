"""Transformation Plugin that uses the Celery framework to call remote workers."""
import os
from typing import TYPE_CHECKING, Dict, Literal

from celery import Celery
from celery.result import AsyncResult
from pydantic import ConfigDict, Field
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


class SessionUpdateCelery(SessionUpdate):
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

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateCelery:
        """Run a job, return a job ID."""
        if session:
            self._use_session(session)

        result: "Union[AsyncResult, Any]" = CELERY_APP.send_task(
            **self.transformation_config.configuration.model_dump()
        )
        return SessionUpdateCelery(celery_task_id=result.task_id)

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize a job."""
        return SessionUpdate()

    def status(self, task_id: str) -> TransformationStatus:
        """Get job status."""
        result = AsyncResult(id=task_id, app=CELERY_APP)
        return TransformationStatus(id=task_id, status=result.state)

    def _use_session(self, session: "Dict[str, Any]") -> None:
        """Update the configuration with values from the sesssion.

        Check all fields (non-aliased and aliased) in `CeleryConfig` if they exist in
        the session. Override the given field values in the current strategy-specific
        configuration (the `CeleryConfig` instance) with the values found in the
        session.

        Parameters:
            session: The current OTE session.

        """
        alias_mapping: dict[str, str] = {
            getattr(field, "alias", field_name): field_name
            for field_name, field in CeleryConfig.model_fields.items()
        }

        fields = set(CeleryConfig.model_fields)
        fields |= {_.alias for _ in CeleryConfig.model_fields.values() if _.alias}

        for field in fields:
            if field in session:
                setattr(
                    self.transformation_config.configuration,
                    alias_mapping[field],
                    session[field],
                )
