"""Test serialise strategies."""


def test_serialise_json():
    """Test `text/json` serialise strategy."""
    from oteapi.datacache import DataCache
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.plugins import create_strategy

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }
    cache = DataCache()
    key = cache.add(data, tag="test")

    config = ResourceConfig(mediaType="text/json", configuration={"accessKey": key})
    serialiser = create_strategy("serialise", config)
    dct = serialiser.parse()
    value = dct["key"]
    print(value)

    assert value == data
