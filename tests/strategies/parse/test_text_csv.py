import csv
import json
from pathlib import Path
from typing import Any, Type

import pytest

from oteapi.strategies.parse.text_csv import CSVParseStrategy

csv_sample_files = [
    (
        "sample1.csv",
        {"dialect": {"skipinitialspace": True, "quoting": "QUOTE_NONNUMERIC"}},
        [
            "Month",
            "Average",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
        ],
        [str, float] + [int] * 11,
    ),
    (
        "sample2.csv",
        {
            "dialect": {
                "skipinitialspace": True,
                "quoting": "QUOTE_NONNUMERIC",
                "base": "excel",
            }
        },
        ["Name", "Team", "Position", "Height(inches)", "Weight(lbs)", "Age"],
        [str] * 3 + [int] * 2 + [float],
    ),
    (
        "sample3.csv",
        {
            "dialect": {
                "skipinitialspace": True,
                "quoting": "QUOTE_NONNUMERIC",
                "base": "unix",
            }
        },
        ["Game Number", "Game Length"],
        [int] * 2,
    ),
    (
        "sample4.csv",
        {"dialect": {"skipinitialspace": True, "quoting": "QUOTE_NONNUMERIC"}},
        ["Game Number", "Game Length"],
        [int] * 2,
    ),
]


@pytest.mark.parametrize(
    "sample_filename,extra_config,headers,types",
    csv_sample_files,
    ids=[_[0].split(".csv", maxsplit=1)[0] for _ in csv_sample_files],
)
def test_csv(
    static_files: Path,
    sample_filename: str,
    extra_config: dict[str, Any],
    headers: list[str],
    types: list[Type],
) -> None:
    """Test `text/csv` parse strategy on local file."""
    sample_file = static_files / sample_filename

    config = {
        "downloadUrl": sample_file.as_uri(),
        "mediaType": "text/csv",
    }
    config.update({"configuration": extra_config} if extra_config else {})

    # Initialize and parse the CSV file
    parser = CSVParseStrategy(config)
    parsed_content = parser.get().content

    kwargs = {}
    if extra_config:
        kwargs.update(extra_config.get("dialect", {}))
        kwargs.update(extra_config.get("reader", {}))

    # Open the CSV file and compare with parsed content
    with open(sample_file, newline="", encoding="utf8") as handle:
        test_data = csv.DictReader(handle, **kwargs)

        # Check if headers match
        assert list(parsed_content.keys()) == test_data.fieldnames == headers

        # Check data types and values
        for index, row in enumerate(test_data):
            for field in test_data.fieldnames:
                types_index = list(parsed_content).index(field)
                assert (
                    isinstance(parsed_content[field][index], types[types_index])
                    or parsed_content[field][index]
                    == parser.parse_config.configuration.reader.restval
                ), (
                    f"Expected type {types[types_index]} or "
                    f"{parser.parse_config.configuration.reader.restval}, but instead "
                    f"got type {type(parsed_content[field][index])} for value "
                    f"{parsed_content[field][index]}. Line index: {index+2}."
                )
                if parsed_content[field][
                    index
                ] != parser.parse_config.configuration.reader.restval and (
                    (row[field] or row[field] == 0.0 or row[field] == 0)
                    and row[field] != kwargs.get("restval", None)
                ):
                    assert (
                        types[types_index](row[field]) == parsed_content[field][index]
                    ), (
                        f"\nfield: {field}\n\nindex: {index}\n\nrow: {row}\n\n"
                        f"parsed_content: {json.dumps(parsed_content, indent=2)}\n"
                    )
                else:
                    print(
                        f"\nfield: {field}\nindex: {index}\nrow: {row}\nparsed: "
                        f"{parsed_content[field][index]!r}"
                    )


def test_csv_dialect_enum_fails() -> None:
    """Test `CSVDialect` is created properly and raises for invalid dialect Enum."""
    from pydantic import ValidationError

    non_existant_dialect = "test"

    config = {
        "downloadUrl": "file:///test.csv",
        "mediaType": "text/csv",
        "configuration": {"dialect": {"base": non_existant_dialect}},
    }

    with pytest.raises(ValidationError) as exception:
        CSVParseStrategy(config)

    assert "ValidationError" in exception.__class__.__name__
