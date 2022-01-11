import sys
from pathlib import Path

thisdir = Path(__file__).absolute().parent
sys.path.insert(1, str(thisdir.parent.parent.parent))

from app.models.resourceconfig import ResourceConfig
from app.strategy.iparsestrategy import create_parse_strategy


def test_json():
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
    parser = create_parse_strategy(config)
    json = parser.parse()

    assert json == data
