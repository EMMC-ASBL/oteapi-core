"""Tests the transformation strategy for Celery."""
# pylint: disable=invalid-name
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from celery import Celery
    from celery.contrib.testing.worker import TestWorkController


@pytest.fixture(scope="session")
def celery_config() -> dict[str, str]:
    """Set Celery fixture configuration."""
    import os

    import redis

    host = os.getenv("OTEAPI_REDIS_HOST", "localhost")
    port = int(os.getenv("OTEAPI_REDIS_PORT", "6379"))
    client = redis.Redis(host=host, port=port)
    try:
        client.ping()
    except redis.ConnectionError:
        if os.getenv("CI"):  # And OS is Linux!
            pytest.fail("In CI environment - this test MUST run !")
        else:
            pytest.skip(f"No redis connection at {host}:{port} for testing celery.")

    return {
        "broker_url": f"redis://{host}:{port}",
        "result_backend": f"redis://{host}:{port}",
    }


def test_celery_remote(
    celery_app: "Celery",
    celery_worker: "TestWorkController",
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test `celery/remote` transformation strategy."""
    from time import sleep, time

    from celery.result import AsyncResult

    from oteapi.models.transformationconfig import TransformationConfig
    from oteapi.strategies.transformation import celery_remote

    @celery_app.task
    def add(x: float, y: float) -> float:
        """Simple addition task to test Celery."""
        return x + y

    celery_worker.reload()

    # Use the test celery app instead of the strategy's celery app
    # The strategy's celery app has not registered the `add()` task...
    monkeypatch.setattr(celery_remote, "CELERY_APP", celery_app)

    config = TransformationConfig(
        transformationType="celery/remote",
        configuration={
            "name": add.name,
            "args": [1, 2],
        },
    )
    transformation = celery_remote.CeleryRemoteStrategy(config)

    session = transformation.initialize({})
    session = transformation.get(session)

    assert session.get("celery_task_id", "")

    start_time = time()
    while (
        transformation.status(session.celery_task_id).status != "SUCCESS"
        and time() < start_time + 5
    ):
        sleep(1)

    if transformation.status(session.celery_task_id).status != "SUCCESS":
        pytest.fail("Status never changed to 'SUCCESS' !")

    result = AsyncResult(id=session.celery_task_id, app=celery_app)
    assert result.result == add(1, 2)
