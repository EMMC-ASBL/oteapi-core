"""Test `oteapi.utils.paths` module."""

import pytest


def test_uri_to_path() -> None:
    """Test `uri_to_path()`."""
    from pathlib import Path
    from urllib.parse import urlparse

    from pydantic import BaseModel, FileUrl

    from oteapi.utils.paths import uri_to_path

    class MyModel(BaseModel):
        """Test pydantic model."""

        parsed_uri: FileUrl

    path_to_this_file = Path(__file__).resolve()
    this_file_as_uri = path_to_this_file.as_uri()

    for uri in (
        this_file_as_uri,
        urlparse(this_file_as_uri),
        MyModel(parsed_uri=this_file_as_uri).parsed_uri,
    ):
        path = uri_to_path(uri)
        assert path.resolve() == path_to_this_file


def test_uri_to_path_warning() -> None:
    """Check a warning is raised when scheme is not 'file'."""
    from pathlib import Path

    from oteapi.utils.paths import uri_to_path

    path_to_this_file = Path(__file__).resolve()
    uri = path_to_this_file.as_uri()

    # Change scheme from 'file' to 'sftp' and explicitly add host ('localhost')
    uri = uri.replace("file:///", "sftp://localhost/")

    with pytest.warns(UserWarning, match=r"A 'file'-scheme was expected.*"):
        path = uri_to_path(uri)
    assert path == path_to_this_file
