"""Tests the parse strategy for JSON."""


def test_json():
    """Test `application/json` parse strategy on 'sample2.json',
    downloaded from filesamples.com.
    """
    from pathlib import Path

    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.application_json import JSONDataParseStrategy

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }

    uri = (Path(__file__).resolve().parents[1] / "sample2.json").as_uri()
    # uri now starts with "file:///..." (incompatible with AnyUrl)
    # On Windows, the drive is also present, e.g. "file:///C:/...",
    # so the second ":" must be removed to produce a valid AnyUrl
    url = uri.replace(":", "").replace("///", "://")
    config = ResourceConfig(
        downloadUrl=url,
        mediaType="application/json",
    )
    parser = JSONDataParseStrategy(config)

    assert parser.get() == data
