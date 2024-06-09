from .base import BaseETL
import os
from tqdm import tqdm
from ..logger_config import logger
import pandas as pd


class NAEBETL(BaseETL):
    def extract(self, raw_data_path: os.PathLike):
        """
        Extract data from the NPASS datasets.

        Parameters:
        raw_data_path (os.PathLike): The path to the raw data directory.
        """
        if not os.path.isdir(raw_data_path):
            raise ValueError("The raw_data_path must be a directory.")

        for root, _, files in os.walk(raw_data_path):
            for file in tqdm(files, desc='Extracting NAEB Datasets...'):
                if file.endswith('.csv'):
                    self.table_info[file.split('.')[0]] = os.path.join(root, file)
                else:
                    continue
        logger.info("Data extracted successfully.")

    def transform(self):
        """ Apply specific transformations for the NPASS data. """
        use = pd.read_csv(self.table_info['uses'])
        use_subcategory = pd.read_csv(self.table_info['use_subcategories'])
        usage = use.merge(use_subcategory, left_on='use_subcategory', right_on='id')
        usage = usage.drop(columns=[
            'pageno',
            'use_category',
            'notes',
            'rawsource',
            'parent',
            'use_subcategory',
            'id_y'
        ])
        usage = usage.rename(columns={
            'id_x': 'use_id',
            'species': 'species_id',
            'tribe': 'tribe_id',
            'source': 'source_id',
            'name': 'usage_name',
        })

        species = pd.read_csv(self.table_info['species'])
        species = species.drop(columns=['usda_code'])
        species = species.rename(columns={'id': 'species_id'})
        species['name'] = species['name'].apply(lambda x: ' '.join(x.split()[:2]))
        species = species.rename(columns={'name': 'species_name'})

        sources = pd.read_csv(self.table_info['sources'])
        sources = sources.drop(columns=['fulltext', 'address', 'school'])
        sources = sources.rename(columns={'id': 'source_id'})

        self.tables = {
            'usage': usage,
            'species': species,
            'sources': sources,
        }




