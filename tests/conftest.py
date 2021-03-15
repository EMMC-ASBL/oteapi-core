#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests.conftest
import pysftp
import pytest

from fastapi.testclient import TestClient
from main import app
from typing import Dict, Generator

import pysftp

from environs import Env

env = Env()
env.read_env()


def pytest_configure(config):
    config.addinivalue_line("markers", "redis: mark test related to Redis")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def sftpconnection() -> Generator:
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(
        host=env.str("SFTP_HOST"),
        username=env.str("SFTP_USER"),
        password=env.str("SFTP_PASSWORD"),
        port=env.int("SFTP_PORT"),
        cnopts=cnopts,
    ) as sftp:
        yield sftp

