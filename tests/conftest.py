"""Pytest fixtures for all tests.

Tests are used for tresting code under development, so we want the
import statements in the tests to import the modules from the source
code, i.e. the local oteapi-core git repository that the tests are a
part of.

Note that if oteapi-core has been installed, the modules would have
been loaded from 'site-packages' in the Python installation instead,
and if oteapi-core hasn't been installed, they would not have been
found at all.
"""
from pathlib import Path

import pytest
from pytest import MonkeyPatch


@pytest.fixture(scope="session", autouse=True)
def import_oteapi_modules() -> None:
    """Set oteapi path to the path of the oteapi source code."""
    m_p = MonkeyPatch()
    m_p.syspath_prepend(str(Path(__file__).absolute().parents[1]))
