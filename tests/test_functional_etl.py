import pytest
import pytest_asyncio
from io import BytesIO
from flottille.etl.pipeline import ETLPipeline
from flottille.etl.extractors.csv_extractor import CSVExtractor
from flottille.etl.transformers.noop_transformer import NoOpTransformer
from flottille.etl.loaders.bytesio_loader import BytesIOLoader

@pytest_asyncio.fixture
async def pipeline():
    # Sample CSV data in BytesIO format
    csv_data = BytesIO(b"Name,Age\nAlice,30\nBob,25")

    # Create the ETL components
    extractor = CSVExtractor(csv_data)
    transformer = NoOpTransformer()
    loader = BytesIOLoader()

    # Instantiate the ETL pipeline with the components
    return ETLPipeline(
        extractors={"csv_extractor": extractor},
        transformers={"noop_transformer": transformer},
        loaders={"bytesio_loader": loader}
    ), loader


@pytest.mark.asyncio
async def test_functional_etl_pipeline(pipeline):
    """
    Functional test for the ETL pipeline that uses the CSVExtractor,
    NoOpTransformer, and BytesIOLoader.
    """
    etl_pipeline, loader = pipeline

    # Run the ETL pipeline
    await etl_pipeline.run()

    # Verify the loaded output
    output = loader.output.getvalue().decode('utf-8')

    # Expected output CSV format
    expected_output = "Name,Age\r\nAlice,30\r\nBob,25\r\n"

    assert output == expected_output, f"Expected: {expected_output}, but got: {output}"
