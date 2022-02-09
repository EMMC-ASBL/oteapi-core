"""Tests the download strategy for 'sftp://'."""
# pylint: disable=no-self-use
import pytest


class MockSFTPConnection:
    """A mockup of pysftp.Connection, as used in SFTPStrategy.get()."""

    from pathlib import Path

    def __init__(self, **kwargs) -> None:
        """Dummy initializer."""

    def __enter__(self):
        """Entry into context manager."""
        return self

    def __exit__(self, exc_type: str, exc_value: str, traceback: str) -> None:
        """Dummy exit from context manager."""

    def get(self, remotepath: str, localpath: Path) -> None:
        """A mockup of pysftp.Connection.get() as called in
        SFTPStrategy.get().
        """
        from shutil import copyfile

        copyfile(remotepath, localpath)


def test_sftp(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test `sftp.py` download strategy by mocking download, and
    comparing data mock downloaded from the local file
    'sample_1280_853.jpeg' with data obtained from simply opening the
    file directly.
    """
    from pathlib import Path

    import pysftp
    from pydantic import AnyUrl

    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.download.sftp import SFTPStrategy

    path = Path(__file__).resolve().parents[1] / "sample_1280_853.jpeg"
    config = ResourceConfig(
        downloadUrl=AnyUrl(url="dummy", scheme="sftp", path=str(path)),
        mediaType="image/jpeg",
    )
    monkeypatch.setattr(pysftp, "Connection", MockSFTPConnection)
    output = SFTPStrategy(config).get()
    content = DataCache().get(output["key"])
    DataCache().clear()
    assert content == path.read_bytes()
