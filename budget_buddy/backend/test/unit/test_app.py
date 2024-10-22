from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import pytest

# pylint: disable=unused-import
from app import app


@pytest.mark.asyncio
async def test_lifespan_and_initialization():
    mock_conn = MagicMock()

    # Patch duckdb.connect to return a mock connection
    with patch("duckdb.connect", return_value=mock_conn):
        # Use TestClient to test the app (this will trigger the lifespan event automatically)
        with TestClient(app) as client:
            # Ensure the SQL was executed
            mock_conn.execute.assert_called_with(
                """
                CREATE TABLE IF NOT EXISTS transaction (
                    id INTEGER PRIMARY KEY,
                    card TEXT,
                    posting_date DATE,
                    description TEXT,
                    amount DECIMAL(10, 2),
                    type TEXT,
                    category TEXT,
                    balance DECIMAL(10, 2)
                )
                """
            )
            # Ensure the health endpoint works
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    # Ensure the database connection was closed after lifespan ends
    mock_conn.close.assert_called_once()


def test_get_transactions():
    client = TestClient(app)
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchall.return_value = []

    with patch("app.get_db", return_value=iter([mock_conn])):
        response = client.get("/transactions")
        assert response.status_code == 200
        assert response.json() == {"transactions": []}
