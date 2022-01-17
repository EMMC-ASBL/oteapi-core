"""Test parse strategies."""


def test_json():
    """Test `text/json` parse strategy."""
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.text_json import JSONDataParseStrategy

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }

    config = ResourceConfig(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="text/json",
    )
    parser = JSONDataParseStrategy(config)
    json = parser.parse()

    assert json == data
