import psycopg
import pytest

from oteapi.strategies.parse.postgres import PostgresResourceStrategy


@pytest.mark.parametrize(
    "query,expected",
    sqlite_queries,
    ids=["user_id=19", "user_id=72"],
)
def test_postgres(
    query: str,
    expected: tuple,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test `application/vnd.postgresql` parse strategy with different SQL queries."""

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
    def mock_connect(connect_str):
        return MockPsycopg()

    monkeypatch.setattr(psycopg, "connect", mock_connect)

    # Configuration for the PostgresResourceStrategy
    config = {
        "accessUrl": "postgresql://postgres:postgres@localhost:5432/postgres",
        "accessService": "foo",
        "configuration": {
            "sqlquery": query,
        },
    }

    # Initialize the PostgresResourceStrategy
    resource_strategy = PostgresResourceStrategy(config)
    resource_strategy.initialize()

    # Execute the SQL query and get the result
    result = resource_strategy.get()

    # Ensure that the result matches the expected output
    assert result.result[0] == expected
