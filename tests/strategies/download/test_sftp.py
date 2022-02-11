"""Tests the download strategy for 'sftp://'."""
# pylint: disable=no-self-use
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import MonkeyPatch


class MockSFTPConnection:
    """A mockup of pysftp.Connection, as used in SFTPStrategy.get()."""

    def __init__(self, **kwargs) -> None:
        """Dummy initializer passing through any kwargs."""

    def __enter__(self):
        """Entry into context manager."""
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        """Dummy exit from context manager."""

    def get(self, remotepath: str, localpath: "Path") -> None:
        """A mockup of pysftp.Connection.get() as called in SFTPStrategy.get()."""
        from shutil import copyfile

        copyfile(remotepath, localpath)


def test_sftp(monkeypatch: "MonkeyPatch", static_files: "Path") -> None:
    """Test `sftp.py` download strategy by mocking download, and comparing data mock
    downloaded from a local file with data obtained from opening the file directly."""
    import pysftp

    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.sftp import SFTPStrategy

    monkeypatch.setattr(pysftp, "Connection", MockSFTPConnection)

    sample_file = static_files / "sample_1280_853.jpeg"

    config = ResourceConfig(
        downloadUrl=f"sftp://{sample_file}",
        mediaType="image/jpeg",
    )

    datacache_key = SFTPStrategy(config).get().get("key", "")
    datacache = DataCache()
    content = datacache.get(datacache_key)
    del datacache[datacache_key]
    assert content == sample_file.read_bytes()
