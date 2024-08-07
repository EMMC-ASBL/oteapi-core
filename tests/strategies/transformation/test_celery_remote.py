"""Tests the transformation strategy for Celery."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture()
def _skip_if_no_docker_or_windows() -> None:
    """Skip a test if `docker` is not available."""
    import platform
    from subprocess import run

    docker_exists = run(["docker", "--version"], check=False).returncode == 0

    is_windows = platform.system() == "Windows"

    if is_windows or not docker_exists:
        pytest.skip("Docker is not available or using Windows!")


@pytest.mark.usefixtures("_skip_if_no_docker_or_windows")
def test_celery_remote(
    celery_setup: CeleryTestSetup,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test `celery/remote` transformation strategy."""
    from time import sleep, time

    from celery.result import AsyncResult

    from oteapi.strategies.transformation import celery_remote

    assert celery_setup.ready()

    # Use the test celery app instead of the strategy's celery app
    # The strategy's celery app has not registered the `add()` task...
    monkeypatch.setattr(celery_remote, "CELERY_APP", celery_setup.app)

    args = [1, 2]

    config = {
        "transformationType": "celery/remote",
        "configuration": {
            "task_name": "pytest_celery.vendors.worker.tasks.add",
            "args": args,
        },
    }
    transformation = celery_remote.CeleryRemoteStrategy(config)

    session = transformation.get()

    assert session.get("celery_task_id", "")

    start_time = time()
    while (
        transformation.status(session.celery_task_id).status != "SUCCESS"
        and time() < start_time + 5
    ):
        sleep(1)

    if (status := transformation.status(session.celery_task_id).status) != "SUCCESS":
        pytest.fail(f"Status never changed to 'SUCCESS'! Status: {status}")

    result = AsyncResult(id=session.celery_task_id, app=celery_setup.app)
    assert result.result == sum(args)


def test_celery_config_name() -> None:
    """Check `CeleryConfig` can be populated with/-out alias use."""
    from oteapi.strategies.transformation.celery_remote import CeleryConfig

    aliased_keys = ("task_name", "args")
    non_aliased_keys = ("name", "args")

    values = ("app.add", [1, 2])

    assert CeleryConfig(**dict(zip(aliased_keys, values))) == CeleryConfig(
        **dict(zip(non_aliased_keys, values))
    )
