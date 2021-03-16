import tempfile

import pandas as pd
import pysftp
import pytest


def test_sftp_connection(sftpconnection: pysftp.Connection) -> None:
    df = pd.DataFrame(dict(a=[1, 2], b=[3, 4]))

    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + "/1.csv"
        df.to_csv(filename)
        sftpconnection.put(localpath=filename)

    assert "1.csv" in sftpconnection.listdir()  # nosec
