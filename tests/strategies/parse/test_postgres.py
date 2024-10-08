"""Tests the parse strategy for SQLite."""

from __future__ import annotations

import pytest

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
    ("query", "expected"),
    sqlite_queries,
    ids=["user_id=19", "user_id=72"],
)
def test_postgres(
    query: str,
    expected: tuple,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test `application/vnd.postgresql` parse strategy with different SQL queries."""
    import psycopg

    from oteapi.strategies.parse.postgres import PostgresParserStrategy

    # Define a mock psycopg connection class
    class MockPsycopg:
        result: tuple

        def cursor(self):
            return self

        def execute(self, query):
            result = [q[1] for q in sqlite_queries if q[0] == query]
            self.result = result
            return self

        def fetchall(self):
            return self.result

        def close(self):
            return

    # Mock the psycopg.connect method
    def mock_connect(connect_str: str) -> MockPsycopg:  # noqa: ARG001
        return MockPsycopg()

    monkeypatch.setattr(psycopg, "connect", mock_connect)

    # Configuration for the PostgresParserStrategy
    config = {
        "parserType": "parser/postgres",
        "entity": "http://onto-ns.com/meta/0.4/example_iri",
        "configuration": {
            "sqlquery": query,
            "accessUrl": "postgresql://postgres:postgres@localhost:5432/postgres",
            "accessService": "postgres",
        },
    }

    # Execute the SQL query and get the result
    result = PostgresParserStrategy(config).get()

    # Ensure that the result matches the expected output
    assert result.result[0] == expected
