from typing import List
from flottille.etl import Transformer

class NoOpTransformer(Transformer):
    async def transform(self, data: List[dict]) -> List[dict]:
        """
        Performs no transformation, returns the data unchanged.
        """
        return data
