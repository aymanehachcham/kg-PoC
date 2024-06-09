import os
from tqdm import tqdm
from .base import BaseETL
from typing import Union
from dotenv import load_dotenv
import chembl_downloader

load_dotenv()


class ChemblETL(BaseETL):
    def extract(self, raw_data_path: Union[os.PathLike, str]) -> None:
        """
        Extract data from the Chembl database.

        Parameters:
        raw_data_path (os.PathLike): The path to the raw data directory.
        """
        if not raw_data_path.endswith('.db'):
            raise ValueError("The raw_data_path must be a SQLite database.")

        self.selected_tables = [
            'CHEMBL_ID_LOOKUP',
            'COMPOUND_RECORDS',
            'TARGET_DICTIONARY',
            'DOCS'
        ]

    def transform(self):
        """ Apply specific transformations for the CHembl data. """
        for table in self.selected_tables:
            sql = f"SELECT * FROM {table} LIMIT 3000"
            self.tables[table] = chembl_downloader.query(sql)