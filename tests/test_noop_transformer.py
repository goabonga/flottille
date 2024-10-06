import pytest
from flottille.etl.transformers.noop_transformer import NoOpTransformer

@pytest.mark.asyncio
async def test_noop_transformer():
    # Sample data to be transformed (though no transformation will be applied)
    data = [
        {"Name": "Alice", "Age": "30"},
        {"Name": "Bob", "Age": "25"}
    ]

    # Create the transformer instance
    transformer = NoOpTransformer()

    # Perform the transformation (No-Op)
    transformed_data = await transformer.transform(data)

    # The transformed data should be the same as the input data
    assert transformed_data == data, f"Expected: {data}, but got: {transformed_data}"
