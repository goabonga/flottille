import csv
from io import BytesIO
from typing import List
from flottille.etl import Extractor

class CSVExtractor(Extractor):
    def __init__(self, file: BytesIO):
        self.file = file

    async def extract(self) -> List[dict]:
        """
        Reads a CSV file from a BytesIO object and returns a list of dictionaries.
        Each row in the CSV will be represented as a dictionary.
        """
        self.file.seek(0)  # Reset the BytesIO position
        reader = csv.DictReader(self.file.read().decode('utf-8').splitlines())
        self.file.seek(0)
        return [row for row in reader]
