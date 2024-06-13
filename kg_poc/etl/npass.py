from .base import BaseETL
import os
import pandas as pd
from tqdm import tqdm
from ..logger_config import logger


class NPASSETL(BaseETL):

    def extract(self, raw_data_path: os.PathLike):
        """
        Extract data from the NPASS datasets.

        Parameters:
        raw_data_path (os.PathLike): The path to the raw data directory.
        """
        if not os.path.isdir(raw_data_path):
            raise ValueError("The raw_data_path must be a directory.")

        for root, _, files in os.walk(raw_data_path):
            for file in tqdm(files, desc='Extracting NPASS Datasets...'):
                if file.endswith('.txt'):
                    self.table_info[file.split('.')[0]] = os.path.join(root, file)
                else:
                    continue
        logger.info("Data extracted successfully.")

    def transform(self):
        """ Apply specific transformations for the NPASS data. """
        target_name = pd.read_csv(self.table_info['NPASS_target_name'], sep='\t')
        target_activity = pd.read_csv(self.table_info['NPASS_targets_activity'], sep='\t')
        target = target_name.merge(target_activity, left_on='target_id', right_on='target_id')
        np_species = pd.read_csv(self.table_info['NPASS_taxonomy_species'], sep='\t')
        np = pd.read_csv(self.table_info['NPASS_natural_product_species'], sep='\t')
        natural_product = np.merge(np_species, left_on='org_id', right_on='org_id')
        compound = pd.read_csv(self.table_info['NPASS_compound_names'], sep='\t')
        # remove duplicates
        target = target.drop_duplicates()
        natural_product = natural_product.drop_duplicates()
        compound = compound.drop_duplicates()

        target = target.dropna()
        natural_product = natural_product.dropna()
        compound = compound.dropna()

        self.tables = {
            'target': target,
            'natural_product': natural_product,
            'compound': compound,
        }
