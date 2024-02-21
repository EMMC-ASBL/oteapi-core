"""Tests the download strategy for 'sftp://'."""

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
        from pathlib import Path, PureWindowsPath
        from shutil import copyfile

        remote_as_path = Path(remotepath)
        if isinstance(remote_as_path, PureWindowsPath):
            remote_as_path = Path(str(remote_as_path).lstrip("\\"))

        copyfile(remote_as_path, localpath)


def test_sftp(monkeypatch: "MonkeyPatch", static_files: "Path") -> None:
    """Test `sftp.py` download strategy by mocking download, and comparing data mock
    downloaded from a local file with data obtained from opening the file directly."""
    import pysftp

    from oteapi.datacache.datacache import DataCache
    from oteapi.strategies.download.sftp import SFTPStrategy

    monkeypatch.setattr(pysftp, "Connection", MockSFTPConnection)

    sample_file = static_files / "sample_1280_853.jpeg"

    config = {
        "downloadUrl": sample_file.as_uri().replace("file:///", "sftp://localhost/"),
        "mediaType": "image/jpeg",
    }

    # Call the strategy and get the datacache key
    datacache_key: str = SFTPStrategy(config).get().get("key", "")

    # Retrieve the content from the datacache using the key
    datacache = DataCache()
    content = datacache.get(datacache_key)

    # Assert that the content matches the content of the original file
    assert content == sample_file.read_bytes()
