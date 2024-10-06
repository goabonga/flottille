import pytest
from flottille.etl.factory import ETLPipelineFactory
from flottille.etl.pipeline import ETLPipeline


# Mock Extractor, Transformer, and Loader classes
class MockExtractor:
    def __init__(self, *args, **kwargs):
        pass

class MockTransformer:
    def __init__(self, *args, **kwargs):
        pass

class MockLoader:
    def __init__(self, *args, **kwargs):
        pass


@pytest.fixture
def mock_pipeline_components():
    mock_extractor = MockExtractor()
    mock_transformer = MockTransformer()
    mock_loader = MockLoader()

    return {
        'extractors': {"mock_extractor": mock_extractor},
        'transformers': {"mock_transformer": mock_transformer},
        'loaders': {"mock_loader": mock_loader}
    }


def test_etl_pipeline_factory_create_pipeline(mock_pipeline_components):
    factory = ETLPipelineFactory()

    # Create a configuration that references the mock classes
    config = {
        'extractors': {
            'extractor1': {
                'class': 'tests.test_etl_pipeline_factory.MockExtractor',
                'params': {}
            }
        },
        'transformers': {
            'transformer1': {
                'class': 'tests.test_etl_pipeline_factory.MockTransformer',
                'params': {}
            }
        },
        'loaders': {
            'loader1': {
                'class': 'tests.test_etl_pipeline_factory.MockLoader',
                'params': {}
            }
        }
    }

    # Run the pipeline creation logic
    pipeline = factory.create_pipeline(config)

    # Check that pipeline was created correctly and that the real components are used
    assert isinstance(pipeline, ETLPipeline)
    assert 'extractor1' in pipeline.extractors
    assert 'transformer1' in pipeline.transformers
    assert 'loader1' in pipeline.loaders

    # Ensure the real components were assigned (not mocks)
    assert isinstance(pipeline.extractors['extractor1'], MockExtractor)
    assert isinstance(pipeline.transformers['transformer1'], MockTransformer)
    assert isinstance(pipeline.loaders['loader1'], MockLoader)
