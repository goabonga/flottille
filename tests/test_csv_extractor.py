import pytest
from io import BytesIO
from flottille.etl.extractors.csv_extractor import CSVExtractor

@pytest.mark.asyncio
async def test_csv_extractor():
    # Sample CSV data in BytesIO format
    csv_data = BytesIO(b"Name,Age\nAlice,30\nBob,25")

    # Create the extractor instance
    extractor = CSVExtractor(csv_data)

    # Extract the data
    data = await extractor.extract()

    # Expected extracted data
    expected_data = [
        {"Name": "Alice", "Age": "30"},
        {"Name": "Bob", "Age": "25"}
    ]

    assert data == expected_data, f"Expected: {expected_data}, but got: {data}"
