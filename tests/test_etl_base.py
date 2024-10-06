import pytest
from flottille.etl import Loader, Transformer, Extractor

# Test for Loader abstract class
@pytest.mark.asyncio
async def test_loader_abstract_method():
    # Try to instantiate a subclass without implementing the abstract method, expect a TypeError
    class IncompleteLoader(Loader):
        pass

    with pytest.raises(TypeError):
        IncompleteLoader()


@pytest.mark.asyncio
async def test_loader_not_implemented_error():
    # Create a subclass that calls the parent abstract method to raise NotImplementedError
    class IncompleteLoader(Loader):
        async def load(self, data):
            return await super().load(data)  # This will raise NotImplementedError

    incomplete_loader = IncompleteLoader()

    with pytest.raises(NotImplementedError):
        await incomplete_loader.load([])


# Test for Transformer abstract class
@pytest.mark.asyncio
async def test_transformer_abstract_method():
    # Try to instantiate a subclass without implementing the abstract method, expect a TypeError
    class IncompleteTransformer(Transformer):
        pass

    with pytest.raises(TypeError):
        IncompleteTransformer()


@pytest.mark.asyncio
async def test_transformer_not_implemented_error():
    # Create a subclass that calls the parent abstract method to raise NotImplementedError
    class IncompleteTransformer(Transformer):
        async def transform(self, data):
            return await super().transform(data)  # This will raise NotImplementedError

    incomplete_transformer = IncompleteTransformer()

    with pytest.raises(NotImplementedError):
        await incomplete_transformer.transform([])


# Test for Extractor abstract class
@pytest.mark.asyncio
async def test_extractor_abstract_method():
    # Try to instantiate a subclass without implementing the abstract method, expect a TypeError
    class IncompleteExtractor(Extractor):
        pass

    with pytest.raises(TypeError):
        IncompleteExtractor()


@pytest.mark.asyncio
async def test_extractor_not_implemented_error():
    # Create a subclass that calls the parent abstract method to raise NotImplementedError
    class IncompleteExtractor(Extractor):
        async def extract(self):
            return await super().extract()  # This will raise NotImplementedError

    incomplete_extractor = IncompleteExtractor()

    with pytest.raises(NotImplementedError):
        await incomplete_extractor.extract()
