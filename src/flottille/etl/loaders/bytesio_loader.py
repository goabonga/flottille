import csv
from io import BytesIO, TextIOWrapper
from typing import List
from flottille.etl import Loader


class BytesIOLoader(Loader):
    def __init__(self):
        self.output = BytesIO()

    async def load(self, data: List[dict]) -> BytesIO:
        """
        Loads data into a BytesIO object in CSV format and returns the BytesIO object.
        """
        # Wrap the BytesIO with TextIOWrapper to handle string encoding
        text_io = TextIOWrapper(self.output, encoding='utf-8', newline='')
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(text_io, fieldnames=fieldnames)

        # Write the header and rows
        writer.writeheader()
        writer.writerows(data)

        # Flush the wrapper to ensure all data is written to BytesIO, but don't close it
        text_io.flush()
        text_io.detach()  # Detach TextIOWrapper so it doesn't close BytesIO

        # Reset the BytesIO position for reading
        self.output.seek(0)
        return self.output