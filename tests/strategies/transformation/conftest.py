"""Pytest fixtures for transformation strategy tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def default_rabbitmq_broker_image() -> str:
    """Pin RabbitMQ to 3.x to avoid RabbitMQ 4.x removing transient_nonexcl_queues."""
    return "rabbitmq:3"
