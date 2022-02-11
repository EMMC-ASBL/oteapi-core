"""Tests the parse strategy for SQLite."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Tuple


sqlite_queries = [
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 19;",
        (
            19,
            "jenny0988",
            "maria",
            "morgan",
            "Female",
            "ec9ed18ae2a13fef709964af24bb60e6",
            1,
        ),
    ),
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 72;",
        (
            72,
            "brown84",
            "john",
            "ross",
            "Male",
            "738cb4da81a2790a9a845f902a811ea2",
            1,
        ),
    ),
]


@pytest.mark.parametrize(
    "query,expected", sqlite_queries, ids=["configuration", "session"]
)
def test_sqlite(
    query: str,
    expected: "Tuple[int, str, str, str, str, str, int]",
    static_files: "Path",
) -> None:
    """Test `application/vnd.sqlite3` parse strategy on a local SQLite DB.

    Test both passing in the query as a configuration and through a session.
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.application_vnd_sqlite import SqliteParseStrategy

    sample_file = static_files / "sample1.db"

    config = ResourceConfig(
        downloadUrl=sample_file.as_uri(),
        mediaType="application/vnd.sqlite3",
        configuration={"sqlquery": query} if "19" in query else {},
    )

    parser = SqliteParseStrategy(config)
    parser.initialize()

    result = parser.get({"sqlquery": query} if "19" not in query else None)

    assert result["result"][0] == expected
