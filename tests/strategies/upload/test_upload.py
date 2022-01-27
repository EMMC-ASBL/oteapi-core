"""Test upload strategies."""
import pytest


@pytest.fixture
def datacache():
    """Setup/teardown fixture for datacache."""
    from oteapi.datacache import DataCache

    cache = DataCache()
    yield cache
    cache.evict(tag="test")


def test_upload_file(datacache):
    """Test file upload strategy."""
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
    key = datacache.add(data, tag="test")

    config = ResourceConfig(
        accessUrl="file://tmp.txt",
        accessService="<unused>",  # Not used!!!
        configuration={"accessKey": key},
    )

    serialiser = create_strategy("upload", config)
    output = serialiser.parse()
    value = output["key"]
    print(value)

    assert value == data
