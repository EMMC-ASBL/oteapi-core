"""Tests the download strategy for 'sftp://'."""
# pylint: disable=unused-argument
# pylint: disable=no-self-use
from pathlib import Path
from shutil import copyfile
from typing import Any

from pydantic import AnyUrl
from pytest_mock import MockerFixture


class MockSFTPConnection:
    """A mockup of pysftp.Connection, as used in SFTPStrategy.get()."""

    def __enter__(self) -> Any:
        """Entry into context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Dummy exit from context manager."""

    def get(self, remotepath: str, localpath: Path) -> None:
        """A mockup of pysftp.Connection.get() as called in
        SFTPStrategy.get().
        """
        copyfile(remotepath, localpath)


def test_sftp(import_oteapi_modules, mocker: MockerFixture) -> None:
    """Test `sftp.py` download strategy by mocking download, and
    comparing data mock downloaded from the local file
    'sample_1280_853.jpeg' with data obtained from simply opening the
    file directly.
    """
    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.sftp import SFTPStrategy

    path = str(Path(__file__).resolve().parents[1] / "sample_1280_853.jpeg")
    config = ResourceConfig(
        accessUrl=AnyUrl(url="dummy", scheme="sftp", path=path),
        accessService="dummy",
    )
    mocker.patch(
        target="pysftp.Connection",
        return_value=MockSFTPConnection(),
    )
    output = SFTPStrategy(config).get()
    content = DataCache().get(output["key"])
    with open(path, "rb") as target:
        assert content == target.read()
