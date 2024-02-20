from time import sleep, time

import pytest
from celery.result import AsyncResult

from oteapi.strategies.transformation.celery_remote import CeleryRemoteStrategy


def test_celery_remote(celery_app, celery_worker, monkeypatch):
    @celery_app.task
    def add(x: float, y: float) -> float:
        """Simple addition task to test Celery."""
        return x + y

    celery_worker.reload()

    # Mock the Celery app to use the test celery app instead of the strategy's celery app
    monkeypatch.setattr(CeleryRemoteStrategy, "CELERY_APP", celery_app)

    # Configuration for the transformation strategy
    config = {
        "transformationType": "celery/remote",
        "configuration": {
            "task_name": add.name,
            "args": [1, 2],
        },
    }

    # Initialize the Celery strategy with the configuration
    transformation = CeleryRemoteStrategy(config)

    # Initialize the job
    session = transformation.initialize({})

    # Submit the job
    session = transformation.get()

    # Check if the Celery task ID is returned
    assert session.get("celery_task_id", "")

    # Check the status of the job until it completes or until timeout (5 seconds)
    start_time = time()
    while (
        transformation.status(session.celery_task_id).status != "SUCCESS"
        and time() < start_time + 5
    ):
        sleep(1)

    # Verify if the job completed successfully
    if transformation.status(session.celery_task_id).status != "SUCCESS":
        pytest.fail("Status never changed to 'SUCCESS' !")

    # Get the result of the Celery task
    result = AsyncResult(id=session.celery_task_id, app=celery_app)

    # Verify the result
    assert result.result == add(1, 2)
