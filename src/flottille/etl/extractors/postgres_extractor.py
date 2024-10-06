from flottille.etl import Extractor
from typing import Any

class PostgresExtractor(Extractor):
    def __init__(self, client):
        self.client = client

    async def extract(self, query: str) -> Any:
        async with self.client.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetch(query)
        return result
