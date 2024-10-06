import asyncio
from typing import Dict, List
from . import Extractor,Transformer, Loader

class ETLPipeline:

    def __init__(self, extractors: Dict[str, Extractor], transformers: Dict[str, Transformer], loaders: Dict[str, Loader], transformer_dependencies: Dict[str, List[str]] = None):
        self.extractors = extractors
        self.transformers = transformers
        self.loaders = loaders
        self.transformer_dependencies = transformer_dependencies or {}

    async def run(self) -> None:
        # Run all extractors in parallel
        extracted_data = await asyncio.gather(*[extractor.extract() for name, extractor in self.extractors.items()])
        
        # Flatten the list of extracted data (if each extractor returns a list)
        extracted_data = [item for sublist in extracted_data for item in sublist]

        # Handle transformer dependencies
        transformed_data = await self.run_transformers(extracted_data)


        #transformed_data = extracted_data

        # Run all transformers
        #for name, transformer in self.transformers.items():
        #    transformed_data = await transformer.transform(transformed_data)

        # Run all loaders
        await asyncio.gather(*[loader.load(transformed_data) for name, loader in self.loaders.items()])

    async def run_transformers(self, data):
        # Track transformer completion
        completed = {}
        
        # Function to run transformers while respecting dependencies
        async def run_transformer(name, transformer, data):
            # If dependencies exist, wait for them
            dependencies = self.transformer_dependencies.get(name, [])
            for dep in dependencies:
                await completed[dep]  # Wait for the dependent transformer to complete
            
            # Run the transformer
            transformed_data = await transformer.transform(data)
            completed[name] = asyncio.create_task(asyncio.sleep(0))  # Mark as completed
            return transformed_data

        # Initialize with the input data
        transformed_data = data

        # Run each transformer, respecting dependencies
        for name, transformer in self.transformers.items():
            transformed_data = await run_transformer(name, transformer, transformed_data)

        return transformed_data
