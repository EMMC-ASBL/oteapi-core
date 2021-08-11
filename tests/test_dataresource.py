import os
import tempfile

import pandas as pd
import pysftp
import pytest
from fastapi.testclient import TestClient

from main import app
from ontotrans.datasource import DataSourceContext
from routers.dataresource import ResourceConfig

SFTP_HOST = os.environ["SFTP_HOST"]
SFTP_USER = os.environ["SFTP_USER"]
SFTP_PASSWORD = os.environ["SFTP_PASSWORD"]
SFTP_PORT = int(os.environ["SFTP_PORT"])


def test_post_dataresource(client: TestClient) -> None:
    response = client.post(
        "/dataresource/",
        json=dict(downloadUrl="http://example.com/1", mediaType="plain/text"),
    )
    resource_info = {
        "uri": "http://example.com/1",
        "media_type": "plain/text",
        "scheme": "http",
        "netloc": "example.com",
        "path": "/1",
        "username": None,
        "password": None,
        "hostname": "example.com",
        "port": None,
    }

    assert response.status_code == 200  # nosec
    assert response.json()["resource_info"] == resource_info  # nosec


def test_post_dataresource_sftp(client: TestClient) -> None:
    response = client.post(
        "/dataresource/",
        json=dict(
            downloadUrl=f"sftp://{SFTP_USER}:{SFTP_PASSWORD}@{SFTP_HOST}:{SFTP_PORT}/file.csv",
            mediaType="text/csv",
        ),
    )
    assert response.status_code == 200  # nosec


@pytest.mark.xfail
def test_post_dataresource_unsupported_mediatype(client: TestClient) -> None:
    response = client.post(
        "/dataresource/",
        json=dict(downloadUrl="http://example.com/2", mediaType="myformat"),
    )
    assert response.status_code == 415  # nosec


def test_get_dataresource_sftp(client: TestClient) -> None:
    response = client.post(
        "/dataresource/",
        json=dict(
            downloadUrl=f"sftp://{SFTP_USER}:{SFTP_PASSWORD}@{SFTP_HOST}:{SFTP_PORT}/file.csv",
            mediaType="text/csv",
        ),
    )
    response = client.get(
        f"/dataresource/{response.json()['resource_id']}",
    )
    assert response.status_code == 200  # nosec


def test_sftp_roundtrip(client: TestClient) -> None:
    df = pd.DataFrame(dict(a=[1, 2], b=[3, 4]))

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + "/1.csv"
        df.to_csv(filename, index=None)
        with pysftp.Connection(
            host=SFTP_HOST,
            username=SFTP_USER,
            password=SFTP_PASSWORD,
            port=SFTP_PORT,
            cnopts=cnopts,
        ) as sftpconnection:
            sftpconnection.put(localpath=filename)
            assert "1.csv" in sftpconnection.listdir()  # nosec

    response = client.post(
        "/dataresource/",
        json=dict(
            downloadUrl=f"sftp://{SFTP_USER}:{SFTP_PASSWORD}@{SFTP_HOST}:{SFTP_PORT}/1.csv",
            mediaType="text/csv",
        ),
    )
    assert response.status_code == 200  # nosec

    # get dataresource
    response = client.get(
        f"/dataresource/{response.json()['resource_id']}",
    )
    assert response.status_code == 200  # nosec

    # read dataresource
    ds = DataSourceContext(
        uri=response.json()["uri"], mediaType=response.json()["media_type"]
    )

    assert ds.read().to_csv() == df.to_csv()  # nosec
