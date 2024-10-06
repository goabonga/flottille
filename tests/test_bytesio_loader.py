import pytest
from flottille.etl.loaders.bytesio_loader import BytesIOLoader

@pytest.mark.asyncio
async def test_bytesio_loader():
    # Sample data to be loaded
    data = [
        {"Name": "Alice", "Age": "30"},
        {"Name": "Bob", "Age": "25"}
    ]

    # Create the loader instance
    loader = BytesIOLoader()

    # Load the data into the BytesIO object
    output = await loader.load(data)

    # Verify the output CSV format
    expected_output = "Name,Age\r\nAlice,30\r\nBob,25\r\n"
    actual_output = output.getvalue().decode('utf-8')

    assert actual_output == expected_output, f"Expected: {expected_output}, but got: {actual_output}"
