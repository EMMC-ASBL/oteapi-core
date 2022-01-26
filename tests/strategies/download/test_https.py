"""Tests the download strategy for 'https://' and 'http://'."""
from pathlib import Path

import requests_mock


@requests_mock.Mocker(kw="mock", real_http=False)
def mock_get(**kwargs):
    """Override requests.get() in 'https.py' by fetching data from
    the local file 'file' instead.
    """
    with open(kwargs["file"], "rb") as f:
        kwargs["mock"].get(kwargs["url"], content=f.read())
    return kwargs["strategy"].get(kwargs["url"])


def test_https(import_oteapi_modules, requests_mock):
    """Test `https.py` download strategy by mocking downloads and
    comparing data mock downloaded from the local copies
    'sample_1280_853.jpeg' and 'sample2.json'
    with data obtained from simply opening them directly.
    """
    from oteapi.datacache.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.plugins.factories import create_download_strategy
    from oteapi.strategies.download.https import HTTPSStrategy

    tests = (
        ("http", "image/jpeg", "sample_1280_853.jpeg"),
        ("https", "image/jpeg", "sample_1280_853.jpeg"),
        ("http", "application/json", "sample2.json"),
        ("https", "application/json", "sample2.json"),
    )

    path = Path(__file__).resolve().parents[1]
    for n in range(len(tests)):
        rc = ResourceConfig(
            downloadUrl=tests[n][0] + "://this.is.not/real.url",
            mediaType=tests[n][1],
        )
        params = {
            "url": rc.downloadUrl,
            "strategy": create_download_strategy(rc),
            "file": str(path / tests[n][2]),
        }
        keyDict = mock_get(**params)
        mockData = DataCache().get(keyDict["key"])
        DataCache().clear()
        with open(params["file"], "rb") as target:
            targetData = target.read()
        assert mockData == targetData
