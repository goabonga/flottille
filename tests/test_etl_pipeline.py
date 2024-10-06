import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from typing import List

from flottille.etl import Extractor, Transformer, Loader
from flottille.etl.pipeline import ETLPipeline

# Mock Extractor, Transformer, and Loader
class MockExtractor(Extractor):
    async def extract(self) -> List[str]:
        return ["mock_data_1", "mock_data_2"]

class MockTransformer(Transformer):
    async def transform(self, data: List[str]) -> List[str]:
        return [d.upper() for d in data]

class MockLoader(Loader):
    async def load(self, data: List[str]) -> None:
        #assert data == [ 'TRANSFORMED_3','MOCK_DATA_1', 'MOCK_DATA_2']
        return data


@pytest_asyncio.fixture
async def pipeline():
    # Mock components
    extractors = {"mock_extractor": MockExtractor()}
    transformers = {
        "mock_transformer_1": MockTransformer(),
        "mock_transformer_2": MockTransformer(),
        "mock_transformer_3": MockTransformer(),
    }
    loaders = {"mock_loader": MockLoader()}

    transformer_dependencies = {
        "mock_transformer_3": ["mock_transformer_1", "mock_transformer_2"]
    }

    return ETLPipeline(
        extractors=extractors, 
        transformers=transformers, 
        loaders=loaders, 
        transformer_dependencies=transformer_dependencies
    )

@pytest.mark.asyncio
async def test_etl_pipeline_with_dependencies(pipeline):
    """
    Test that the ETL pipeline works with transformer dependencies.
    """
    await pipeline.run()


@pytest.mark.asyncio
async def test_transformer_dependencies_are_respected(pipeline):
    """
    Test that transformers with dependencies are executed in the correct order.
    """
    mock_transformer_1 = AsyncMock()
    mock_transformer_2 = AsyncMock()
    mock_transformer_3 = AsyncMock()

    # Simulate transformation results
    mock_transformer_1.transform = AsyncMock(return_value=["mock_data_1_transformed_1"])
    mock_transformer_2.transform = AsyncMock(return_value=["mock_data_1_transformed_2"])
    mock_transformer_3.transform = AsyncMock(return_value=["TRANSFORMED_3"])

    pipeline.transformers = {
        "mock_transformer_1": mock_transformer_1,
        "mock_transformer_2": mock_transformer_2,
        "mock_transformer_3": mock_transformer_3,
    }

    await pipeline.run()

    # Check if transformer3 waited for transformer1 and transformer2
    mock_transformer_1.transform.assert_called_once()
    mock_transformer_2.transform.assert_called_once()
    mock_transformer_3.transform.assert_called_once()

    # Ensure transformer3 is executed after transformer1 and transformer2
    assert mock_transformer_3.transform.call_args[0][0] == ["mock_data_1_transformed_2"]


@pytest.mark.asyncio
async def test_loader_is_called_with_dependencies(pipeline):
    """
    Test that the loader's `load` method is called with transformed data from all transformers.
    """
    mock_loader = AsyncMock()
    pipeline.loaders = {"mock_loader": mock_loader}

    await pipeline.run()

    # Check that the loader received the final transformed data from transformer3
    mock_loader.load.assert_called_once_with(["MOCK_DATA_1","MOCK_DATA_2"])
