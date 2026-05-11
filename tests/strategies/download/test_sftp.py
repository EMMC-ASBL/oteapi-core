"""Tests the download strategy for 'sftp://'."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


class MockSFTPClient:
    """A mockup of paramiko.SFTPClient, as used in SFTPStrategy.get()."""

    def __enter__(self):
        """Entry into context manager."""
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Dummy exit from context manager."""

    def get(self, remotepath: str, localpath: str) -> None:
        """A mockup of SFTPClient.get() as called in SFTPStrategy.get()."""
        from pathlib import Path, PureWindowsPath
        from shutil import copyfile

        remote_as_path = Path(remotepath)
        if isinstance(remote_as_path, PureWindowsPath):
            remote_as_path = Path(str(remote_as_path).lstrip("\\"))

        copyfile(remote_as_path, localpath)


class MockSSHClient:
    """A mockup of paramiko.SSHClient, as used in SFTPStrategy.get()."""

    def __enter__(self):
        """Entry into context manager."""
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Dummy exit from context manager."""

    def set_missing_host_key_policy(self, _: object) -> None:
        """Dummy set_missing_host_key_policy."""

    def connect(self, **_kwargs: object) -> None:
        """Dummy connect."""

    def open_sftp(self) -> MockSFTPClient:
        """Return a mock SFTP client."""
        return MockSFTPClient()


def test_sftp(monkeypatch: pytest.MonkeyPatch, static_files: Path) -> None:
    """Test `sftp.py` download strategy by mocking download, and comparing data mock
    downloaded from a local file with data obtained from opening the file directly."""
    import paramiko

    from oteapi.datacache.datacache import DataCache
    from oteapi.strategies.download.sftp import SFTPStrategy

    monkeypatch.setattr(paramiko, "SSHClient", MockSSHClient)

    sample_file = static_files / "sample_1280_853.jpeg"

    config = {
        "downloadUrl": sample_file.as_uri().replace("file:///", "sftp://localhost/"),
        "mediaType": "image/jpeg",
    }

    # Call the strategy and get the datacache key
    datacache_key: str = SFTPStrategy(config).get()["key"]
    # Retrieve the content from the datacache using the key
    datacache = DataCache()
    content = datacache.get(datacache_key)
    del datacache[datacache_key]
    # Assert that the content matches the content of the original file
    assert content == sample_file.read_bytes()
