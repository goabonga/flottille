import yaml
from typing import Dict


from .pipeline import ETLPipeline

class ETLPipelineFactory:
    def __init__(self):
        pass

    def create_pipeline(self, config: Dict) -> ETLPipeline:
        # Load extractors
        extractors = {
            name: self._initialize_component(details['class'], details['params'])
            for name, details in config['extractors'].items()
        }

        # Load transformers
        transformers = {
            name: self._initialize_component(details['class'], details['params'])
            for name, details in config['transformers'].items()
        }

        # Load loaders
        loaders = {
            name: self._initialize_component(details['class'], details['params'])
            for name, details in config['loaders'].items()
        }

        return ETLPipeline(extractors=extractors, transformers=transformers, loaders=loaders)

    def _initialize_component(self, class_path: str, params: Dict):
        # Dynamically import the class
        module_path, class_name = class_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        component_class = getattr(module, class_name)
        # Initialize the class with params
        return component_class(**params)



class ETLPipelineYamlFactory(ETLPipelineFactory):
    def __init__(self, config_path: str):
        super().__init__()
        self.config_path = config_path

    def load_config(self) -> Dict:
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def create_pipeline(self) -> ETLPipeline:
        config = self.load_config()
        return super().create_pipeline(config)
