from abc import ABC, abstractmethod
from typing import Any, List


class Extractor(ABC):
    @abstractmethod
    async def extract(self) -> List[Any]:
        """
        Method to extract data from the source.
        Returns a list of objects.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class Transformer(ABC):
    @abstractmethod
    async def transform(self, data: List[Any]) -> List[Any]:
        """
        Method to transform the extracted data.
        Takes a list of objects as input and returns a list of transformed objects.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class Loader(ABC):
    @abstractmethod
    async def load(self, data: List[Any]) -> None:
        """
        Method to load data into the final destination.
        Takes a list of transformed objects.
        """
        raise NotImplementedError("Subclasses must implement this method.")