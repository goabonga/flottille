import pytest
from unittest.mock import patch, mock_open, MagicMock
from flottille.etl.factory import ETLPipelineYamlFactory
from flottille.etl.pipeline import ETLPipeline

@pytest.fixture
def mock_yaml_config():
    return """
    extractors:
      extractor1:
        class: flottille.etl.extractors.MockExtractor
        params: {}
    transformers:
      transformer1:
          class: flottille.etl.transformers.MockTransformer
          params: {}
      transformer2:
          class: flottille.etl.transformers.MockTransformer
          params: {}
      transformer3:
          class: flottille.etl.transformers.MockTransformer
          params: {}
          depends_on: 
          - transformer1
          - transformer2        
    loaders:
      loader1:
        class: flottille.etl.loaders.MockLoader
        params: {}
    """

@pytest.fixture
def mock_pipeline_components():
    mock_extractor = MagicMock()
    mock_transformer = MagicMock()
    mock_loader = MagicMock()

    return {
        'extractors': {"mock_extractor": mock_extractor},
        'transformers': {"mock_transformer": mock_transformer},
        'loaders': {"mock_loader": mock_loader}
    }


@patch("builtins.open", new_callable=mock_open, read_data="yaml content")
@patch("yaml.safe_load")
def test_etl_pipeline_yaml_factory_create_pipeline(mock_safe_load, mock_open, mock_pipeline_components):
    # Directly set mock_safe_load to return the parsed YAML content (as a Python dictionary)
    mock_safe_load.return_value = {
        'extractors': {
            'extractor1': {'class': 'flottille.etl.extractors.MockExtractor', 'params': {}}
        },
        'transformers': {
            'transformer1': {'class': 'flottille.etl.transformers.MockTransformer', 'params': {}}
        },
        'loaders': {
            'loader1': {'class': 'flottille.etl.loaders.MockLoader', 'params': {}}
        }
    }

    factory = ETLPipelineYamlFactory("mock_config.yaml")

    # Mock the _initialize_component method to return mocked components
    def mock_initialize_component(class_path, params):
        if 'extractors' in class_path:
            return mock_pipeline_components['extractors']['mock_extractor']
        elif 'transformers' in class_path:
            return mock_pipeline_components['transformers']['mock_transformer']
        elif 'loaders' in class_path:
            return mock_pipeline_components['loaders']['mock_loader']
        else:
            raise KeyError(f"Unknown class_path: {class_path}")

    with patch.object(factory, '_initialize_component', side_effect=mock_initialize_component):
        pipeline = factory.create_pipeline()

        # Check that pipeline was created correctly and that the mock components are used
        assert isinstance(pipeline, ETLPipeline)
        assert 'extractor1' in pipeline.extractors
        assert 'transformer1' in pipeline.transformers
        assert 'loader1' in pipeline.loaders

        # Ensure the mocked components were assigned
        assert pipeline.extractors['extractor1'] == mock_pipeline_components['extractors']['mock_extractor']
        assert pipeline.transformers['transformer1'] == mock_pipeline_components['transformers']['mock_transformer']
        assert pipeline.loaders['loader1'] == mock_pipeline_components['loaders']['mock_loader']
