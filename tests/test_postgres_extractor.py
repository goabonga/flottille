import pytest
from unittest.mock import AsyncMock, MagicMock
from flottille.etl.extractors.postgres_extractor import PostgresExtractor

@pytest.mark.asyncio
async def test_postgres_extractor():
    # Mock the client and the connection object
    mock_client = MagicMock()
    mock_conn = AsyncMock()

    # Properly mock acquire() to behave as an async context manager
    mock_client.acquire = MagicMock()
    mock_client.acquire().__aenter__.return_value = mock_conn
    mock_client.acquire().__aexit__.return_value = AsyncMock()

    # Simulate the transaction context manager
    mock_conn.transaction = MagicMock()
    mock_conn.transaction().__aenter__.return_value = mock_conn
    mock_conn.transaction().__aexit__.return_value = AsyncMock()

    # Mock the fetch method to return a predefined result
    mock_conn.fetch = AsyncMock(return_value=[{"id": 1, "name": "example"}])

    # Initialize the PostgresExtractor with the mock client
    extractor = PostgresExtractor(client=mock_client)

    # Perform the extract operation
    query = "SELECT * FROM test_table"
    result = await extractor.extract(query)

    # Assertions
    assert result == [{"id": 1, "name": "example"}]
    mock_conn.fetch.assert_called_once_with(query)
