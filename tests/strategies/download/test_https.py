"""Tests the download strategy for 'https://' and 'http://'."""
# pylint: disable=unused-argument
# pylint: disable=unused-import
from pathlib import Path

import requests_mock


@requests_mock.Mocker(kw="mock", real_http=False)
def mock_get(**kwargs):
    """Override requests.get() in 'https.py' by fetching data from
    the local file 'file' instead.
    """
    with open(kwargs["file"], "rb") as args_file:
        kwargs["mock"].get(kwargs["url"], content=args_file.read())
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
    for test in tests:
        res_conf = ResourceConfig(
            downloadUrl=test[0] + "://this.is.not/real.url",
            mediaType=test[1],
        )
        params = {
            "url": res_conf.downloadUrl,
            "strategy": create_download_strategy(res_conf),
            "file": str(path / test[2]),
        }
        key_dict = mock_get(**params)
        mock_data = DataCache().get(key_dict["key"])
        DataCache().clear()
        with open(params["file"], "rb") as target:
            target_data = target.read()
        assert mock_data == target_data
