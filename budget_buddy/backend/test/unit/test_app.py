from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# pylint: disable=unused-import
from app import app, get_db

client = TestClient(app)


def test_get_transactions():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchall.return_value = []

    with patch("app.get_db", return_value=iter([mock_conn])):
        response = client.get("/transactions")
        assert response.status_code == 200
        assert response.json() == {"transactions": []}
